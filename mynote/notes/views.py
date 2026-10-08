from django.shortcuts import render
from .models import Note
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def creat_note(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    note = Note.objects.create(title = title, content = content)

    return JsonResponse({
        'id': note.id,
        'title' : note.title,
        'content' : note.content,
        'is_complete' : note.is_complete,
    })


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