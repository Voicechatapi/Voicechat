
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse

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

    def get_queryset(self):
        tasks = Task.objects.filter(user=self.request.user)
        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the queryset that was already filtered in get_queryset
        tasks = context['tasks']

        context['count'] = tasks.filter(complete=False).count

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = tasks.filter(title__startswith=search_input)

        context['search_input'] = search_input
        return context
    



class StarterView(LoginView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/starter.html'

