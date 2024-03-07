

from django.urls import path, include
from .views import (
    login, addUser, deleteUser
)
urlpatterns = [
        path('login', login, name='login'),
        path('addUser', addUser, name='addUser'),
        path('deleteUser', deleteUser, name='deleteUser'),
    # Add other URL patterns as needed
]