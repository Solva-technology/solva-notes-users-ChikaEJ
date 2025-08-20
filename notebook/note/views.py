from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .forms.form import NoteForm
from .models import Note

@login_required(login_url='login')
def all_notes(request):
    all_notes = (Note
                 .objects
                 .select_related('author', 'status')
                 .prefetch_related('categories')
                 .order_by('-created_at')
                 )
    context = {'all_notes': all_notes}
    return render(request, 'notes/all_notes.html', context)

@login_required(login_url='login')
def note_detail(request, note_id):
    note = get_object_or_404(
        Note
        .objects
        .select_related('author', 'status')
        .prefetch_related('categories'),
        pk=note_id
    )
    context = {'note': note}
    return render(request, 'notes/note_detail.html', context)

@login_required(login_url='login')
def note_create_update(request, note_id=None):
    note = get_object_or_404(Note, pk=note_id) if note_id else None
    if note is not None:
        if note.author.id != request.user.id and not request.user.is_superuser:
            raise Http404
    if request.method == 'POST':
        note_form = NoteForm(request.POST, instance=note)
        if note_form.is_valid():
            new_note = note_form.save(commit=False)
            if note is None:
                new_note.author = request.user
            new_note.save()
            note_form.save_m2m()
            return redirect('notes:note_detail', note_id=new_note.id)
    else:
        note_form = NoteForm(instance=note)

    return render(
        request,
        'notes/note_form.html',
        {'form': note_form, 'note': note}
    )

@login_required(login_url='login')
def note_delete(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if note.author != request.user:
        raise Http404
    if request.method == 'POST':
        note.delete()
        return redirect('notes:all_notes')

@login_required(login_url='login')
def my_notes(request):
    all_notes = (Note.objects.filter(author=request.user))
    context = {'all_notes': all_notes}
    return render(request, 'notes/my_notes.html', context)