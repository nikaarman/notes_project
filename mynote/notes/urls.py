from django.urls import path
from .views import creat_note, notes_list, delete_note

urlpatterns = [
    path('notes/', creat_note),
    path('notes/all/', notes_list),
    path('notes/<int:id>/', delete_note),
]