

from django.urls import path, include
from .views import (
    login, addUser, deleteUser, activateUser, rolesLookUp, addMaterial, getMaterials, getUsers, changeUserRole
)
urlpatterns = [
        path('login', login, name='login'),
        path('addUser', addUser, name='addUser'),
        path('deleteUser', deleteUser, name='deleteUser'),
        path('activateUser', activateUser, name='activateUser'),
        path('rolesLookUp', rolesLookUp, name='rolesLookUp'),
        path('addMaterial', addMaterial, name='addMaterial'),
        path('getMaterials', getMaterials, name='getMaterials'),
        path('getUsers', getUsers, name='getUsers'),
        path('changeUserRole', changeUserRole, name='changeUserRole'),

        
    # Add other URL patterns as needed
]