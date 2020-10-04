from django.http import HttpResponsePermanentRedirect


class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().partition(':')[0]
        if host == "joincampus.ca" or host == "joincampus.herokuapp.com":
            return HttpResponsePermanentRedirect(
                "https://www.joincampus.ca" + request.path
            )
        else:
            return self.get_response(request)