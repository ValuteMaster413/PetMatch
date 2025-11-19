from dataclasses import asdict

from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from application.create_pet_use_case.create_pet_command import CreatePetCommand
from application.delete_pet_use_case.delete_pet_command import DeletePetCommand
from application.edit_pet_use_case.edit_pet_command import EditPetCommand
from application.list_all_pets_use_case.list_all_pets_query import ListAllPetsQuery
from core.application.common.abstractions.messaging.abstract_mediator import AbstractMediator
from main import container

@csrf_exempt
def create_pet_controller(request):
    mediator = container.get_required(AbstractMediator)

    data = request.POST
    name = data.get("name")
    species = data.get('species')

    command = CreatePetCommand(name, species)

    result = mediator.send(command)

    if result.success:
        return JsonResponse({"data": f"name: {result.content.name}, species: {result.content.species}"})
    else:
        return JsonResponse({"error": result.error.message}, status=500)

@csrf_exempt
def delete_pet_controller(request):
    mediator = container.get_required(AbstractMediator)

    data = request.POST
    name = data.get("name")

    command = DeletePetCommand(name)

    result = mediator.send(command)

    if result.success:
        return JsonResponse({"data": result.content})
    else:
        return JsonResponse({"error": result.error.message}, status=500)

@csrf_exempt
def edit_pet_controller(request, ):
    mediator = container.get_required(AbstractMediator)

    data = request.POST

    old_name = data.get("old_name")
    new_name = data.get("new_name")
    new_species = data.get("new_species")


    command = EditPetCommand(old_name, new_name, new_species)

    result = mediator.send(command)

    if result.success:
        return JsonResponse({"data": result.content})
    else:
        return JsonResponse({"error": result.error.message}, status=500)


def pets_list_controller(request):
    mediator = container.get_required(AbstractMediator)

    command = ListAllPetsQuery()
    result = mediator.send(command)

    if result.success:
        pets = result.content  # это QuerySet или список Pet
        data = [model_to_dict(pet) for pet in pets]

        return JsonResponse({"data": data})
    else:
        return JsonResponse({"error": result.error.message}, status=500)

