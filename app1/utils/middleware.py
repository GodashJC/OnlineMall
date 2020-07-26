from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class LoginMiddleWare(MiddlewareMixin):
    def process_request(self,request):

        #print(request.path)

        if request.path in ["/admin/","/admin/login/","/login/","/reg/",]:
            return None

        if not request.user.id:
            return redirect("/login/")

