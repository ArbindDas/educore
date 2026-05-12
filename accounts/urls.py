from django.urls import path
from . import views

urlpatterns = [

    path(
        'register/principal/',
        views.PrincipalRegisterView.as_view(),
        name='principal-register'
    ),

    path(
        
        'create-user/',
        views.UserCreateView.as_view(),
        name='create-user'
    ),
    
     # ✅ THIS IS REQUIRED (you are missing this)
    path(
        'me/',
        views.MeView.as_view(),
        name='me'
    ),
    
]