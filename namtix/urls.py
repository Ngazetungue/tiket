from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('dashboard', include('organisers.urls')),
    path('accounts/', include('users.urls')),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), 
        name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), 
        name='password_change'),
   
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = "registration/password_reset.html"),
        name='password_reset'),
    
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name = "registration/password_reset_sent.html"),
        name="password_reset_done"),
    
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = "registration/password_reset_form.html"),
        name="password_reset_confirm"),
    
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name = "registration/password_reset_done.html"),
        name="password_reset_complete"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
