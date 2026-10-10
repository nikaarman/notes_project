import json
from django.shortcuts import render
from .models import Note
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_note(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405
        )

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    title = data.get("title")
    content = data.get("content")

    if not isinstance(title, str) or not title.strip():
        return JsonResponse(
            {"error": "Title is required"},
            status=400
        )

    if not isinstance(content, str) or not content.strip():
        return JsonResponse(
            {"error": "Content is required"},
            status=400
        )

    note = Note.objects.create(
        title=title,
        content=content
    )

    return JsonResponse({
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "is_complete": note.is_complete
    }, status=201)

def notes_list(request):
    notes = Note.objects.all()

    if not notes:
        return JsonResponse({
            'massage':'No notes found'
        })
    return JsonResponse({
        'notes': list(notes.values())
    })

@csrf_exempt
def delete_note(request, id):
    if request.method == 'DELETE':
        try:
            note = Note.objects.get(id=id)
            note.delete()

            return JsonResponse({
                'message': 'Note deleted successfully'
            })

        except Note.DoesNotExist:
            return JsonResponse({
                'message': 'Note not found'
            }, status=404)

    return JsonResponse({
        'message': 'Method not allowed'
    }, status=405)

def get_note(request, note_id):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405
        )

    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        return JsonResponse(
            {"error": "Note not found"},
            status=404
        )

    return JsonResponse({
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "is_complete": note.is_complete
    })

@csrf_exempt
def complete_note(request, note_id):
    if request.method != "PATCH":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405
        )

    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        return JsonResponse(
            {"error": "Note not found"},
            status=404
        )

    note.is_complete = True
    note.save(update_fields=["is_complete"])

    return JsonResponse({
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "is_complete": note.is_complete
    })