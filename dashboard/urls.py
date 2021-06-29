from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('notes', views.notes, name='notes'),
    path('delete_note/<int:pk>', views.delete_note, name='delete_note'),
    path('notes/<int:pk>', views.NotesDetailView.as_view(), name='notes_detail'),
    path('homework', views.homework, name='homework'),
    path('update-homework/<int:pk>', views.update_homework, name='update_homework'),
    path('delete_homework/<int:pk>', views.delete_homework, name='delete_homework'),
    path('youtube', views.youtube, name='youtube'),
    path('todo', views.todo, name='todo'),
    path('update-todo/<int:pk>', views.update_todo, name='update_todo'),
    path('delete-todo/<int:pk>', views.delete_todo, name='delete_todo'),
    path('books', views.books, name='books'),
    path('dictionary', views.dictionary, name='dictionary'),
    path('wiki', views.wiki, name='wiki')
]
