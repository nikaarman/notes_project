from django.urls import path
from .views import create_note, notes_list, delete_note
from . import views

urlpatterns = [
    path('notes/', create_note),
    path('notes/all/', notes_list),
    path('notes/<int:id>/', delete_note),
    path("notes/", views.create_note, name="create_note"),
    path("notes/<int:note_id>/", views.get_note, name="get_note"),
    path(
    "notes/<int:note_id>/complete/",
    views.complete_note,
    name="complete_note"
),
]