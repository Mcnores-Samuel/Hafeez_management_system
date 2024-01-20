"""This module contains a view function for
aiding the real time autocomplete
functionality.
"""
from django.http import JsonResponse
from ..models.main_storage import MainStorage


def autocomplete(request, name):
    """This view function is responsible for
    handling the autocomplete functionality.

    Functionality:
    - Checks if the user is authenticated and is an agent. Only agents are allowed
      to access this view.
    - Returns a list of phone names that match the search query.

    Parameters:
    - request: The HTTP request object containing user information.
    - name: The name of the phone to search for.

    Returns:
    - If the user is not authenticated or is not an agent, it returns a 403 Forbidden
      response.
    - If the agent is authenticated and has stock, it returns a list of phone names
      that match the search query.

    Usage:
    Agents access this view to search for phones.
    It ensures that only agents are able to access this view.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='staff_members').exists():
        phones = None
        if name == 'Spark 10C':
            phones = MainStorage.objects.filter(name=name, phone_type='10C').first()
        else:
            phones = MainStorage.objects.filter(name__exact=name).first()
        data = {}
        if phones:
            data["name"] = phones.name
            data["phone_type"] = phones.phone_type
            data["category"] = phones.category
            data["spec"] = phones.spec
            data["screen_size"] = phones.screen_size
            data["os"] = phones.os
            data["battery"] = phones.battery
            data["camera"] = phones.camera
            data["supplier"] = phones.supplier

        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Forbidden'}, status=403)
