from django.urls import path

from infrastructure.controllers import create_pet_controller, delete_pet_controller, edit_pet_controller, pets_list_controller

urlpatterns = [
    path('create', create_pet_controller, name='create'),
    path('delete', delete_pet_controller, name='delete'),
    path('edit', edit_pet_controller, name='edit'),
    path('pets_list', pets_list_controller, name='pets_list'),
]
