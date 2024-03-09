

from django.urls import path, include
from .views import (
    login, addUser, deleteUser, rolesLookUp
)
urlpatterns = [
        path('login', login, name='login'),
        path('addUser', addUser, name='addUser'),
        path('deleteUser', deleteUser, name='deleteUser'),
        path('rolesLookUp', rolesLookUp, name='rolesLookUp'),
    # Add other URL patterns as needed
]