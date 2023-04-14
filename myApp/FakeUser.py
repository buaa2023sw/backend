from myApp.models import User

class FakeUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Create a fake user and set it as the user attribute of the request
        request.user = User.objects.get(id=1)
        return self.get_response(request)