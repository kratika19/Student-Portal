from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic
from .forms import *
from youtubesearchpython import VideosSearch
import requests, wikipedia


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


def youtube(request):
    if request.method == 'POST':
        youtube_form = DashboardForm()
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        # print(video.result()['result'])
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime']
            }
            print(result_dict)
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
        return render(request, 'dashboard/youtube.html', {
            'form': youtube_form,
            'results': result_list
        })
    else:
        youtube_form = DashboardForm()
    return render(request, 'dashboard/youtube.html', {
        'form': youtube_form
    })


def todo(request):
    if request.method == 'POST':
        todoform = TodoForm(request.POST)
        if todoform.is_valid():
            try:
                finish = request.POST['status']
                if finish == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            new_todo = Todo(user=request.user, title=request.POST['title'], status=finished)
            new_todo.save()
            messages.success(request, f'Todo is added by {request.user.username} successfully!')
    else:
        todoform = TodoForm()
    get_todo = Todo.objects.filter(user=request.user)
    length = len(get_todo)
    if length == 0:
        no_todo = True
    else:
        no_todo = False
    return render(request, 'dashboard/todo.html', {
        'todos': get_todo,
        'no_todo': no_todo,
        'form': todoform
    })


def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.status == True:
        todo.status = False
    else:
        todo.status = True

    todo.save()
    return redirect('todo')


def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')


def books(request):
    if request.method == 'POST':
        book_form = DashboardForm()
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink')
            }
            result_list.append(result_dict)
        return render(request, 'dashboard/books.html', {
            'form': book_form,
            'results': result_list
        })
    else:
        book_form = DashboardForm()
    return render(request, 'dashboard/books.html', {
        'form': book_form
    })


def dictionary(request):
    if request.method == 'POST':
        dictionary_form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
        r = requests.get(url)
        answer = r.json()
        print(answer)
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            synonyms = answer[0]['meanings'][0]['definitions'][0].get('synonyms'),
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            context = {
                'form': dictionary_form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definitions': definition,
                'synonyms': synonyms,
                'example': example,
            }
        except:
            context = {
                'form': dictionary_form,
                'input': '',
            }
        return render(request, 'dashboard/dictionary.html', context)
    else:
        dictionary_form = DashboardForm()
        context = {
            'form': dictionary_form
        }
    return render(request, 'dashboard/dictionary.html', context)


def wiki(request):
    if request.method == 'POST':
        wiki_form = DashboardForm(request.POST)
        text = request.POST['text']
        page = wikipedia.page(text)
        try:
            context = {
                'form': wiki_form,
                'title': page.title,
                'link': page.url,
                'summary': page.summary
            }
        except wikipedia.exceptions.PageError as e:
            print(e.options)
            context = {
                "form": wiki_form
            }
        return render(request, 'dashboard/wiki.html', context)

    else:
        wiki_form = DashboardForm()
    return render(request, 'dashboard/wiki.html', {
        'form': wiki_form
    })


def conversion(request):
    if request.method == 'POST':
        conversion_form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form': conversion_form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''

                if input and int(input) > 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input) * 3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input) / 3} yard'
                context = {
                    'form': conversion_form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form': conversion_form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''

                if input and int(input) > 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input) * 0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input) * 2.20462} pound'
                context = {
                    'form': conversion_form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }
    else:
        conversion_form = ConversionForm()
        context = {
            'form': conversion_form,
            'input': False
        }
    return render(request, 'dashboard/conversion.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}!!')
            # return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'dashboard/register.html', {
        'form': form
    })

