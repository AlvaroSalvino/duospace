from django.urls import path
from .views import *

urlpatterns = [
    path('deslogar/', logout_view, name='deslogar'),
    path("login/", login, name="login"),
    path('inscreva-se/', inscrevase, name='inscrevase'),
]