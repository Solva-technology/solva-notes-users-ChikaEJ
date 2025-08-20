from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(
        pattern_name='notes:all_notes',
        permanent=False)
         ),
    path('notes/', include('note.urls')),
    path('users/', include('user.urls')),
]
