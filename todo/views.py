from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import DetailView

from .models import TodoItem
from .forms import TodoForm, TodoDeleteForm, TodoToggleStatusForm

class TodolistView(LoginRequiredMixin, View):
    form_class = TodoForm
    template_name = 'todo_list.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            todo_item = TodoItem()
            todo_item.text = form.cleaned_data['text']
            todo_item.user = request.user
            todo_item.save()
            return redirect('todo_list')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        todo_list = request.user.todoitem_set.order_by('-created')
        context = {
            'todo_list': todo_list,
            'form': form
        }
        return render(request, self.template_name , context)

class TodoActionView(UserPassesTestMixin, View):
    """ class to prefetch a todo item and allow only the related user 
    to do actions on it """
    model_class = TodoItem

    def setup(self, request, *args, **kwargs):
        super(TodoActionView, self).setup(request, *args, **kwargs)
        self.todo_item = get_object_or_404(self.model_class, pk=self.kwargs.get('pk'))

    def test_func(self):
        return self.request.user == self.todo_item.user


class TodoDeleteView(TodoActionView):
    form_class = TodoDeleteForm
    template_name = 'todo_delete.html'

    def post(self, request, *args, **kwargs):
        form = TodoDeleteForm(request.POST)
        if form.is_valid():
            name = self.todo_item.text
            self.todo_item.delete()
            messages.add_message(request, messages.INFO, f'Item {name} has been deleted.')
            return redirect('todo_list')
    
    def get(self, request, *args, **kwargs):
        form = TodoDeleteForm()
        context = {
            'todo_item': self.todo_item,
            'form': form
        }
        return render(request, self.template_name, context)

class TodoToggleView(TodoActionView):
    """ toggle todo item status between completed and not completed """

    def post(self, request, *args, **kwargs):
        form = TodoToggleStatusForm(request.POST)
        if form.is_valid():
            self.todo_item.completed = not self.todo_item.completed
            self.todo_item.save()
            messages.add_message(
                request, messages.INFO, 
                f"Item {self.todo_item.text} has been marked {'completed' if self.todo_item.completed else 'uncompleted'}."
                )
            return redirect('todo_list')