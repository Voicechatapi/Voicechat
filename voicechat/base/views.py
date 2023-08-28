# from typing import Any, Dict
# from django.forms.models import BaseModelForm
# from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CustomUserCreationForm

from .models import Task


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/interface.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        chat_content = request.POST.get('chatContent')
        chat_id = request.POST.get('chat_id')
        chat_name = request.POST.get('chat_name')
        if chat_content:
            if Task.objects.get(id=chat_id).exist():
                task.chatContent += chat_content
            else:
                task = Task.objects.get_or_create(user=request.user)
                task.chatContent = chat_content
                task.chat_id = chat_id
                task.chat_name = chat_name
            task.save()
            
        else:
            response_data = {'status': 'error', 'message': 'Chat content is required.'}
        
        return JsonResponse(response_data)
    

    
class StarterView(LoginView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/starter.html'
