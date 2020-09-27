from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from .models import Animal


class AnimalTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', email='test@email.com', password='secret'
        )

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
        self.animal = Animal.objects.create(animal_name=dog.get('animal_name'), species='dog',
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

    def test_string_representation(self):
        animal = Animal(animal_name='Ася')
        self.assertEqual(animal.__repr__(), f'{animal.animal_name, animal.species}')

    def test_animal_content(self):
        self.assertEqual(f'{self.animal.animal_name}', 'Ася')
        self.assertEqual(f'{self.animal.species}', 'dog')
        self.assertEqual(f'{self.animal.age}', '10')
        self.assertEqual(f'{self.animal.breed}', "метис ВЕО")
        self.assertEqual(f'{self.animal.born}', " март 2011")
        self.assertEqual(f'{self.animal.height}', '50')
        self.assertEqual(f'{self.animal.weight}', '10')
        self.assertEqual(f'{self.animal.lifespan}', '10')
        self.assertEqual(f'{self.animal.temperament}', 'some temperament')
        self.assertEqual(f'{self.animal.had_owner}', 'True')
        self.assertEqual(f'{self.animal.animal_sex}', 'female')
        self.assertEqual(f'{self.animal.profile_link}', 'http://priut-ks.ru/sobaki-v-dar/female/147-Asya')
        self.assertEqual(f'{self.animal.profile_photo_link}', 'http://priut-ks.ru/pic/dogs/147/main/main.jpg')
        self.assertEqual(f'{self.animal.animal_description}', 'Some description')
        self.assertEqual(f'{self.animal.asylum}', 'Red Pine')
        self.assertEqual(f'{self.animal.contact_string}', 'abc.http.de')

    def test_animal_list_view(self):
        response = self.client.get(reverse('animals'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ася')
        self.assertTemplateUsed(response, 'animals.html')

    def test_animal_detail_view(self):
        response = self.client.get('/animal/2/')
        no_response = self.client.get('/animal/666666/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Red Pine')
        self.assertTemplateUsed(response, 'animal_detail.html')
