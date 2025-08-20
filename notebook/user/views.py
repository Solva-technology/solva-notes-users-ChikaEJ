from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms.form import RegisterForm
from .models import UserProfile


@login_required(login_url='login')
def all_users(request):
    users = UserProfile.objects.select_related('user')
    context = {'users': users}
    return render(request, 'users/all_users.html', context)


@login_required(login_url='login')
def user_detail(request, id):
    user_profile = get_object_or_404(
        UserProfile.objects.select_related('user'),
        user__id=id
    )
    return render(
        request,
        'users/user_detail.html',
        {'user_profile': user_profile}
    )


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect("/")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})
