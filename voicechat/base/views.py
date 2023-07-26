from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView,FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


from .models import Task
from django.shortcuts import redirect


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(RegisterPage, self).get(*args, **kwargs)


class CustomLoginView(LoginView):
    template_name = "base/custom_login.html"
    fields='__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

# Create your views here.
class TaskList(PermissionRequiredMixin, ListView):
    model=Task
    context_object_name= 'tasks'

class TaskDetail(PermissionRequiredMixin,DetailView):
    model=Task
    context_object_name='task'
    template_name='base/task.html'

class TaskCreate(PermissionRequiredMixin,CreateView):
    model=Task
    fields='__all__'
    template_name='base/create.html'
    success_url= reverse_lazy('index')

class TaskUpdate(PermissionRequiredMixin,UpdateView):
    model=Task
    fields='__all__'
    template_name='base/create.html'
    success_url= reverse_lazy('index')

class TaskDelete(PermissionRequiredMixin,DeleteView):
    model=Task
    fields='__all__'
    template_name='base/delete.html'
    success_url= reverse_lazy('index')
