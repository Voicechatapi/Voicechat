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
from django.contrib.auth.models import Permission

import json

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


# def save_chat(request):
#     if request.method == 'POST':
#         if not request.user.has_perm('your_app.can_save_chat'):
#             # User does not have permission to save chat
#             raise PermissionDenied
#         data = json.loads(request.body)
#         chat_content = data.get("conversation")  # Correct variable name
#         chat_id = data.get("id")
#         chat_name = data.get("name")
#         try:
#             task = Task.objects.get(id=chat_id)
#             if task:
#                 task.chatContent += chat_content
#                 task.id = chat_id
#                 task.name = chat_name
#                 task.save()
#         except Task.DoesNotExist:
#             task = Task.objects.create(
#                 user=request.user, id=chat_id, chatContent=chat_content, name=chat_name)
#         return JsonResponse({"success": True})
#     else:
#         return JsonResponse({"error": "Invalid HTTP method"}, status=405)

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/interface.html'

    def post(self, request, *args, **kwargs):
        chat_content = request.POST.get('chatContent')
        if not chat_content:
            return JsonResponse({'status': 'error', 'message': 'nochat'})
        chat_id = request.POST.get('chat_id')
        if not chat_id:
        # Chat content is empty, return an error message
            return JsonResponse({'status': 'error', 'message': 'noid'})
        chat_name = request.POST.get('chat_name')
        if chat_content:
            try:
                task = Task.objects.get(id=chat_id)
                if task:
                    task.chatContent += chat_content
                    task.id = chat_id
                    task.name = chat_name
                    task.save()
            except Task.DoesNotExist:
                task = Task.objects.create(user=request.user, id=chat_id, chatContent=chat_content, name=chat_name)
        else:
            response_data = {'status': 'error', 'message': 'Chat content is required.'}
            return JsonResponse(response_data, status=400)

        response_data = {'status': 'success', 'message': 'Chat content saved successfully.'}
        return JsonResponse(response_data)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    # def post(self, request, *args, **kwargs):
    #     chat_content = request.POST.get('chatContent')
    #     chat_id = request.POST.get('chat_id')
    #     chat_name = request.POST.get('chat_name')
    #     if chat_content:
    #         try:
    #             task = Task.objects.get(id=chat_id)
    #             if task:
    #                 task.chatContent += chat_content
    #                 task.id = chat_id
    #                 task.name = chat_name
    #                 task.save()
    #         except Task.DoesNotExist:
    #             task = Task.objects.create(user=request.user, id=chat_id, chatContent=chat_content, name=chat_name)
    #     else:
    #         response_data = {'status': 'error', 'message': 'Chat content is required.'}
    #         return JsonResponse(response_data, status=400)

    #     response_data = {'status': 'success', 'message': 'Chat content saved successfully.'}
    #     return JsonResponse(response_data)


class StarterView(LoginView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/starter.html'
