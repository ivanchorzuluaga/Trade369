from django.shortcuts import redirect 

class AdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.Administrador:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('dashboardUsuario369')