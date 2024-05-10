

from django.urls import path, include
from .views import (
    login, addUser, deleteUser, activateUser, rolesLookUp,
    addMaterial, getMaterials, getUsers, changeUserRole,
    getAvailableMaterials, addProduct, getProducts, getUsersByFilter,
    createQaRequest, getQARequests, acceptQaRequest, completeQaRequest,
    cancelQaRequest, getQaRequest, getStoreProducts, addOrder, getOrders,
    sendOrderForShipping, createShippingRequest, getShippingRequests,
    acceptShippingRequest, completeShippingRequest, cancelShippingRequest,
    getShippingRequest, getSystemLogs, getNotifications

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
        path('getUsersByFilter', getUsersByFilter, name='getUsersByFilter'),
        path('createQaRequest', createQaRequest, name='createQaRequest'),
        path('getQARequests', getQARequests, name='getQARequests'),
        path('acceptQaRequest', acceptQaRequest, name='acceptQaRequest'),
        path('completeQaRequest', completeQaRequest, name='completeQaRequest'),
        path('cancelQaRequest', cancelQaRequest, name='cancelQaRequest'),
        path('getQaRequest', getQaRequest, name='getQaRequest'),
        path('getStoreProducts', getStoreProducts, name='getStoreProducts'),
        path('addOrder', addOrder, name='addOrder'),
        path('getOrders', getOrders, name='getOrders'),
        path('sendOrderForShipping', sendOrderForShipping, name='sendOrderForShipping'),
        path('createShippingRequest', createShippingRequest, name='createShippingRequest'),
        path('getShippingRequests', getShippingRequests, name='getShippingRequests'),
        path('acceptShippingRequest', acceptShippingRequest, name='acceptShippingRequest'),
        path('completeShippingRequest', completeShippingRequest, name='completeShippingRequest'),
        path('cancelShippingRequest', cancelShippingRequest, name='cancelShippingRequest'),
        path('getShippingRequest', getShippingRequest, name='getShippingRequest'),
        path('getSystemLogs', getSystemLogs, name='getSystemLogs'),
        path('getNotifications', getNotifications, name='getNotifications'),



]