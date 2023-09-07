from django.shortcuts import redirect
from django.urls import reverse

class RedirectAuthenticatedUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path == reverse('sign_in'):
            return redirect(reverse('home_page'))
        elif request.user.is_authenticated:
              if not request.user.is_staff and request.path.startswith('/admin/'):
                  return redirect(reverse('home_page'))
        elif request.user.is_authenticated and request.path == reverse('password_reset'):
            return redirect(reverse('home_page'))
        elif request.user.is_authenticated and request.path == reverse('password_reset_done'):
            return redirect(reverse('home_page'))
        return self.get_response(request)