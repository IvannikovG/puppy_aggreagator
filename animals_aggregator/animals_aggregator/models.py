from django.db import models


class Animal(models.Model):
    """ Most general model for an animal so far
    """
    animal_name = models.CharField(max_length=200)
    species = models.CharField(max_length=25)
    age = models.IntegerField(null=True)
    breed = models.CharField(max_length=200, blank=True, null=True)
    born = models.CharField('Date of birth', null=True, blank=True, max_length=50)
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    lifespan = models.IntegerField(null=True)
    temperament = models.CharField(max_length=100, blank=True, null=True)
    had_owner = models.BooleanField(default=False, blank=True, null=True)
    animal_sex = models.CharField(max_length=20, blank=True, null=True)
    profile_link = models.CharField(max_length=300)
    profile_photo_link = models.CharField(max_length=300)
    animal_description = models.CharField(max_length=500, blank=True, null=True)
    asylum = models.CharField(max_length=300)
    contact_string = models.CharField(max_length=300, blank=True, null=True)

    def __repr__(self):
        return f'{self.animal_name, self.species}'

    class Meta:
        ordering = ['animal_name']
