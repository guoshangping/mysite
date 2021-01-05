from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class LoginCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == "GET":
            is_login = request.COOKIES.get("is_login", "")
            if request.path != "/xuanxing/login/" and request.path.startswith("/xuanxing"):
                print(request.path)
                if is_login != "1":
                    return redirect("/xuanxing/login")
