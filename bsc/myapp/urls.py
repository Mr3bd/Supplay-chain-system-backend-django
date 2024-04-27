

from django.urls import path, include
from .views import (
    login, addUser, deleteUser, activateUser, rolesLookUp, 
    addMaterial, getMaterials, getUsers, changeUserRole,
    getAvailableMaterials, addProduct, getProducts
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
        path('getAvailableMaterials', getAvailableMaterials, name='getAvailableMaterials'),
        path('addProduct', addProduct, name='addProduct'),
        path('getProducts', getProducts, name='getProducts'),

        
    # Add other URL patterns as needed
]