from django.urls import  path
from . import views

urlpatterns = [
    path('',views.login369,name='login369'),
    path('logout/',views.cerrarSesion,name='logout'),
    path('dashboard369/',views.dashboard369,name='dashboard369'),
    path('dashboardUsuario369/',views.dashboardUsuario369,name='dashboardUsuario369'),

    path('usuario369/',views.usuario369,name='usuario369'),
    path('editarUsuario369/<id>/', views.editarUsuario369, name="editarUsuario369"),
    path('eliminarUsuario369/<id>/', views.eliminarUsuario369, name="eliminarUsuario369"),

    path('detalleUsuario369/',views.detalleUsuario369,name='detalleUsuario369'),
    path('editarDetalleUsuario369/<id>/', views.editarDetalleUsuario369, name="editarDetalleUsuario369"),
    path('eliminarDetalleUsuario369/<id>/', views.eliminarDetalleUsuario369, name="eliminarDetalleUsuario369"),
    

    path('contrato369/',views.contrato369,name='contrato369'),
    path('editarContrato369/<id>/', views.editarContrato369, name="editarContrato369"),
    path('eliminarContrato369/<id>/', views.eliminarContrato369, name="eliminarContrato369"),

    path('retiro369/',views.retiro369,name='retiro369'),
    path('editarRetiro369/<id>/', views.editarRetiro369, name="editarRetiro369"),
    path('eliminarRetiro369/<id>/', views.eliminarRetiro369, name="eliminarRetiro369"),

    path('valor369/',views.valor369,name='valor369'),
    path('editarValor369/<id>/', views.editarValor369, name="editarValor369"),
    path('eliminarValor369/<id>/', views.eliminarValor369, name="eliminarValor369"),
]
