from django.http import HttpResponseForbidden

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request,*args,**kwargs):
            if request.user.role == role:
                return view_func (request,*args,**kwargs)
            else:
                return HttpResponseForbidden
        return _wrapped_view
    return decorator