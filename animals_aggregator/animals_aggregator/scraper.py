import requests
import requests_html
from typing import List, Iterator, Dict, Any
from concurrent.futures import ProcessPoolExecutor
from bs4 import BeautifulSoup
from abc import abstractmethod
import re


class GettingEngine:
    """ Class with static functions to grab url and parse responses """

    # Send requests
    @staticmethod
    def send_get_request_to_url(url: str, max_level: int = 5) -> requests.Response:
        session = requests_html.HTMLSession()
        result = session.get(url)
        return result

    @staticmethod
    def get_all_responses_from(urls: List[str]) -> Iterator[requests.Response]:
        with ProcessPoolExecutor(4) as executor:
            results = executor.map(GettingEngine.send_get_request_to_url, urls)
            return results

    # Some small helpers
    @staticmethod
    def get_html(response: requests.Response):
        return response.text

    @staticmethod
    def parse_height(height: str) -> int:
        words = height.split(' ')
        return int(list(filter(lambda x: str.isdigit(x), words))[0])

    @staticmethod
    @abstractmethod
    def get_animal_sex(string: Any) -> str:
        pass

    # DOG RELATED
    @staticmethod
    @abstractmethod
    def parse_animal_info(dog) -> Dict:
        pass

    @staticmethod
    @abstractmethod
    def parse_response(response: requests.Response) -> List[Dict]:
        pass


class RedPineEngine(GettingEngine):

    @staticmethod
    def get_animal_sex(string: str) -> str:
        words = string.split('/')
        try:
            sex = words[-2]
            if sex in ['puppy', 'female', 'male']:
                return sex
        except Exception:
            sex = ''
            return sex

    @staticmethod
    def parse_response(response: requests.Response) -> List[Dict]:
        html = RedPineEngine.get_html(response)
        soup = BeautifulSoup(html, 'html.parser')
        dogs = soup.main.find_all(id='dog')
        parsed_dogs_info = [RedPineEngine.parse_animal_info(dog) for dog in dogs]
        return parsed_dogs_info

    @staticmethod
    def parse_animal_info(dog) -> Dict:
        """ Returns a dog info dictionary """
        info_in_a_tag = dog.find('a')
        image_link = dog.find('img')
        dog_personal_link = f"http://priut-ks.ru{info_in_a_tag.get('href')}"
        dog_photo_link = f"http://priut-ks.ru{image_link.get('src')}"
        dog_stats = dog.find_all('span')
        dog_info = {
            'animal_name': dog_stats[0].contents[0],
            'breed': dog_stats[1].contents[0],
            'born': dog_stats[2].contents[0],
            'height': RedPineEngine.parse_height(dog_stats[3].contents[0]),
            'profile_link': dog_personal_link,
            'profile_photo_link': dog_photo_link,
            'animal_sex': RedPineEngine.get_animal_sex(dog_personal_link),
            'asylum': 'Red Pine'
        }
        return dog_info


class AsylumBiruylevoEngine(GettingEngine):

    @staticmethod
    def get_animal_sex(animal) -> str:
        container = animal.find('span', {'class': 'gender'}).contents[0]
        try:
            sex = container.contents[1]
            if sex.lower() == 'девочка':
                animal_sex = 'Female'
            elif sex.lower() == 'мальчик':
                animal_sex = 'Male'
            else:
                animal_sex = None
        except Exception:
            animal_sex = ''
        return animal_sex

    @staticmethod
    def parse_response(response: requests.Response) -> List[Dict]:
        html = AsylumBiruylevoEngine.get_html(response)
        soup = BeautifulSoup(html, 'html.parser')
        animals = soup.findAll("div", {'class': 'card box'})
        return animals

    @staticmethod
    def is_owned(animal_description: str) -> bool:
        """ Shows if the dog is owned by someone
            But not 100 reliable :)
        """
        key_words = list(map(lambda x: x.lower(), ['Передержка', 'передержки',
                                                   'Передержке', 'передержку',]))
        return any(key_word in animal_description for key_word in key_words)

    @staticmethod
    def get_possible_age(animal_description: str) -> str:
        """ Shows possible age if it is written in description """

        try:
            import re
            description = animal_description.split(' ')
            possible_age = min(list(filter(lambda x: float(x), description)))
            return possible_age
        except Exception:
            return ''

    @staticmethod
    def send_get_request_to_url(url: str, max_level: int = 5, cookies=True) -> requests.Response:
        if cookies:
            cookie = {f'level{num}': '1' for num in range(1, max_level + 1)}
        session = requests_html.HTMLSession()
        result = session.get(url, cookies=cookie)
        return result

    @staticmethod
    def get_animal_species(url: str) -> str:
        try:
            words = url.split('/')
            species = words[1]
            if species == 'sobaki':
                species = 'dog'
            elif species == 'koshki':
                species = 'cat'
            else:
                species = None
        except Exception:
            species = ''
        return species

    @staticmethod
    def parse_animal_info(animal: Dict) -> Dict:
        info_in_a_tag = animal.find('a')
        animal_name = animal.find('h2').find('a').contents[0]
        image_link = animal.find('img')
        animal_link = info_in_a_tag.get('href')
        animal_personal_link = f"http://www.izpriuta.ru{animal_link}"
        animal_photo_link = image_link.get('src').split('?')[0]
        animal_description = animal.find('h4').contents[0]
        animal_info = {
            'animal_name': animal_name,
            'species': AsylumBiruylevoEngine.get_animal_species(animal_link),
            'had_owner': AsylumBiruylevoEngine.is_owned(animal_description),
            'animal_sex': AsylumBiruylevoEngine.get_animal_sex(animal),
            'profile_link': animal_personal_link,
            'profile_photo_link': animal_photo_link,
            'animal_description': animal_description,
            'asylum': 'asylum_biruylevo',
            'age': None,
        }
        return animal_info


class HelpDogEngine(GettingEngine):

    @staticmethod
    def get_animal_sex(animal) -> str:
        pass

    @staticmethod
    def parse_response(response: requests.Response) -> List[Dict]:
        html = AsylumBiruylevoEngine.get_html(response)
        soup = BeautifulSoup(html, 'html.parser')
        animals = soup.findAll("div", {'class': 'individual-pet'})
        return animals

    @staticmethod
    def parse_animal_info(animal: Dict) -> Dict:
        animal_data = animal.find('ul')
        list_items = [item for item in animal_data.find_all('li')]
        contents_array = []
        for item in list_items:
            animal_property = re.compile('[^a-zA-Z]').sub('', item.contents[0]).lower()
            try:
                animal_contents = animal_property, item.contents[1].contents[0]
            except:
                animal_contents = animal_property, ''
            contents_array.append(animal_contents)

        animal_contents = dict(contents_array)
        profile_link = ''
        profile_photo_link = animal.find('img').get('src')
        animal_description = ''
        contact_string = animal.find('p').contents[0]

        animal_info = {
            'animal_name': animal_contents.get('name'),
            'species': 'dog',
            'age': animal_contents.get('age'),
            'breed': '',
            'born': '',
            'height': animal_contents.get('height'),
            'weight': animal_contents.get('weight'),
            'lifespan': animal_contents.get('lifespan'),
            'temperament': animal_contents.get('temperament'),
            'had_owner': False,
            'animal_sex': '',
            'profile_link': profile_link,
            'profile_photo_link': profile_photo_link,
            'animal_description': animal_description,
            'asylum': 'HelpDog',
            'contact_string': contact_string,
        }
        return animal_info


if __name__ == '__main__':
    hde = HelpDogEngine()
    responses = HelpDogEngine.get_all_responses_from(['https://helpdog.ru'])
    for resp in responses:

        for item in HelpDogEngine.parse_response(resp):
            # print(item)
            print(HelpDogEngine.parse_animal_info(item))
            break



