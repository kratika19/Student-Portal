from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic
from .forms import *
from .models import Homework


# Create your views here.

def home(request):
    return render(request, 'dashboard/home.html')


def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            new_note = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            new_note.save()
        messages.success(request, f"Notes is Added from {request.user.username} successfully")

    else:
        form = NotesForm()

    all_notes = Notes.objects.filter(user=request.user)
    return render(request, 'dashboard/notes.html', {
        'all_notes': all_notes,
        'note_form': form
    })


def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


class NotesDetailView(generic.DetailView):
    model = Notes
    context_object_name = 'note'


def homework(request):
    all_homework = Homework.objects.filter(user=request.user)
    left_homework = Homework.objects.filter(user=request.user, is_finished=False)
    if len(left_homework) == 0:
        done = True
    else:
        done = False
    return render(request, 'dashboard/homework.html', {
        'homeworks': all_homework,
        'done': done
    })
