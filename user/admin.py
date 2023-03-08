from django.contrib import admin
from user.models import User, cliente, contrato, retiro,valores
# Register your models here.
admin.site.register(User)
admin.site.register(cliente)
admin.site.register(contrato)
admin.site.register(retiro)
admin.site.register(valores)