from django.shortcuts import HttpResponse
from . import scraper
from . import models
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

t_urls = [
    'http://priut-ks.ru/sobaki-v-dar/female',
    'http://priut-ks.ru/sobaki-v-dar/male',
    'http://priut-ks.ru/sobaki-v-dar/puppy',
    'http://priut-ks.ru/sobaki-v-horoshie-ruki'
]


def update_redpine_dogs(request):
    responses = scraper.RedPineEngine.get_all_responses_from(t_urls)
    for resp in responses:
        dogs = scraper.RedPineEngine.parse_response(resp)
        for dog in dogs:
            dog_entry = models.Animal(animal_name=dog.get('animal_name'), species='dog',
                                      age=dog.get('age'), breed=dog.get('breed'),
                                      born=dog.get('born'),
                                      height=dog.get('height'), weight=dog.get('weight'),
                                      lifespan=dog.get('lifespan'), temperament=dog.get('temperament'),
                                      had_owner=dog.get('had_owner'), animal_sex=dog.get('animal_sex'),
                                      profile_link=dog.get('profile_link'),
                                      profile_photo_link=dog.get('profile_photo_link'),
                                      animal_description=dog.get('animal_description'),
                                      asylum=dog.get('asylum'),
                                      contact_string=dog.get('contact_string'))

            dog_entry.save()

    return HttpResponse('Animals were updated to red_pine')


class AnimalListView(ListView):
    model = models.Animal
    template_name = 'animals.html'


class AnimalDetailView(DetailView):
    model = models.Animal
    template_name = 'animal_detail.html'
    context_object_name = 'animal'


class AnimalCreateView(CreateView):
    model = models.Animal
    template_name = 'animal_new.html'
    fields = '__all__'


class AnimalUpdateView(UpdateView):
    pass