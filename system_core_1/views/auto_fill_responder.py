from django.http import JsonResponse
from ..models.main_storage import MainStorage

def get_item_data(request):
    if request.is_ajax() and request.method == 'GET':
        item_id = request.GET.get('item_id', None)
        data = MainStorage.objects.get(id=item_id).values()
        data = list(data)
        return JsonResponse(data)