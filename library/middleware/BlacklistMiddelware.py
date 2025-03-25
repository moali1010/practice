from django.http.response import HttpResponseForbidden


def get_client_ip(request):
    pass


blacklist = ...


class BlacklistMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip = get_client_ip(request)
        if client_ip in blacklist:
            return HttpResponseForbidden()

        response = self.get_response(request)
        return response
