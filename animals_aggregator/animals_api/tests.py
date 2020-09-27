from django.test import TestCase
from animals_aggregator.models import Animal


class AnimalModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        dog = {
            "id": 1,
            "animal_name": "Ася",
            "species": "dog",
            "age": 10,
            "breed": "метис ВЕО",
            "born": " март 2011",
            "height": 50,
            "weight": 10,
            "lifespan": 10,
            "temperament": 'some temperament',
            "had_owner": True,
            "animal_sex": "female",
            "profile_link": "http://priut-ks.ru/sobaki-v-dar/female/147-Asya",
            "profile_photo_link": "http://priut-ks.ru/pic/dogs/147/main/main.jpg",
            "animal_description": 'Some description',
            "asylum": "Red Pine",
            "contact_string": 'abc.http.de'
        }
        Animal.objects.create(animal_name=dog.get('animal_name'), species='dog',
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

    def test_name_content(self):
        animal = Animal.objects.get(id=1)
        expected_object_name = f'{animal.animal_name}'
        self.assertEquals(expected_object_name, 'Ася')

    def test_some_content(self):
        animal = Animal.objects.get(id=1)
        expected_temperament_name = f'{animal.temperament}'
        expected_had_owner = animal.had_owner
        self.assertEquals(expected_temperament_name, 'some temperament')
        assert expected_had_owner

