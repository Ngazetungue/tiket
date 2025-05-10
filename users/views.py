from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, FormView

from .forms import CustomUserCreationForm
from .models import CustomUser


def custom_logout(request):
    logout(request)
    return redirect('home')


class SignupPageView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CustomLoginView(FormView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        if user.user_type == 'staff':
            return redirect('organisers:staff-dashboard')
        elif user.user_type == 'organiser':
            return redirect('organisers:organiser-dashboard')
        elif user.user_type == 'admin':
            return redirect('organisers:admin-dashboard')
        
        return redirect(self.success_url)


@method_decorator(login_required, name='dispatch')
class StaffDashboardView(View):
    template_name = 'organisers/staff-dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class OrganiserDashboardView(View):
    template_name = 'organisers/organiser-dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class AdminDashboardView(View):
    template_name = 'organisers/admin-dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)




class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'
