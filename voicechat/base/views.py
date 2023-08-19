
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Task


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')


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


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Your existing context data
        return context

    def post(self, request, *args, **kwargs):
        user_input = request.POST.get('user_input')

        # Set up the data for OpenAI API request
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": user_input}],
            "temperature": 1.0,
        }

        # Make API call to OpenAI
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {API_KEY}',  # Replace API_KEY with your actual API key
            },
            json=data
        )

        # Process the OpenAI API response
        bot_response = ""
        if response.status_code == 200:
            output_data = response.json()
            bot_response = output_data['choices'][0]['message']['content']
        else:
            bot_response = "Sorry, I'm having trouble reaching the OpenAI API at the moment."

        # Save the chat history to the database
        # ... (your code to save chat history)

        return JsonResponse({'bot_response': bot_response})
    



class StarterView(LoginView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/starter.html'

