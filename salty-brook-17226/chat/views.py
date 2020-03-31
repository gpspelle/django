# chat/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

#from django.contrib import messages
#from django.views.generic import TemplateView


#class ChatView(TemplateView):
#    template_name = 'chat/chat.html'
