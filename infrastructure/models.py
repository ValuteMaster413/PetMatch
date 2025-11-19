from django.db import models

from domain.shared.abstraction.value_objects.pet_uid import PetUID


class Pet(models.Model):
    _id = models.CharField(
        primary_key=True,
        max_length=32,
        editable=False
    )
    name = models.CharField(max_length=200)
    species = models.CharField(max_length=200)
