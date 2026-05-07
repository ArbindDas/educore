from django.urls import path
from . import views

urlpatterns = [

    path(
        'register/principal/',
        views.PrincipalRegisterView.as_view(),
        name='principal-register'
    ),

]