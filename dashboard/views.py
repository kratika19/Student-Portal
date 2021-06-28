from django.shortcuts import render
from .models import Notes


# Create your views here.

def home(request):
    return render(request, 'dashboard/home.html')


def notes(request):
    all_notes = Notes.objects.filter(user=request.user)
    return render(request, 'dashboard/notes.html', {
        'all_notes': all_notes
    })
