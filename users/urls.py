from django.urls import path
from django.contrib.auth.views import ( 
    LoginView, 
    LogoutView,
    
)
from users import views
from .views import SignupPageView, custom_logout


app_name ='users'
urlpatterns = [
    
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    # path('logout/',LogoutView.as_view(), name='logout'),
    path('logout/', custom_logout, name='logout'),

    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
    #     name='password_change_done'),
    # path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), 
    #     name='password_change'),
    
]
