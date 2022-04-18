from typing import List
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from chats.models import Chat, Group
# Create your views here.


class HomeView(ListView):
    model = Group
    context_object_name = 'group_list'
    template_name = 'chats/home.html'

class GroupChatView(DetailView):
    model = Group 
    pk_url_kwarg = 'group_name'
    template_name = 'chats/group_chat.html'

    def get_object(self, queryset =None):
        group_name = self.kwargs.get('group_name').strip().lower()
        group_obj = get_object_or_404(Group, name=group_name)
        return group_obj

    def get_context_data(self, **kwargs): 
        group_name = self.get_object()  
        group = Group.objects.filter(name__iexact = group_name )
        chats = [] 
        if group.exists():
            context = super().get_context_data(**kwargs)
            chats = group.first().chat_set.all() 
        context['chats'] = chats
        context['group_list'] = Group.objects.all() 
        return context 