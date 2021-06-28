from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic
from .forms import *


# from .models import Homework


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
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finish = request.POST['is_finished']
                if finish == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            new_homework = Homework(user=request.user, subject=request.POST['subject'], title=request.POST['title'],
                                    description=request.POST['description'], due_date=request.POST['due_date'],
                                    is_finished=finished)
            new_homework.save()
            messages.success(request, f'Homework is created by {request.user.username} successfully!')
    else:
        form = HomeworkForm()
    all_homework = Homework.objects.filter(user=request.user)
    if len(all_homework) == 0:
        done = True
    else:
        done = False
    return render(request, 'dashboard/homework.html', {
        'homeworks': all_homework,
        'done': done,
        'homework_form': form
    })


def update_homework(request, pk=None):
    get_homework = Homework.objects.get(id=pk)
    if get_homework.is_finished:
        get_homework.is_finished = False
    else:
        get_homework.is_finished = True

    get_homework.save()
    return redirect('homework')


def delete_homework(request, pk):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')
