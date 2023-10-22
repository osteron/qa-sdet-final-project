import allure
import pytest
import requests
from .urls import Url
from .models import GetResponseDogModel, GetResponseListDogModel, GetResponseListBreedsModel
from .. import validate_json, check_status_code


@allure.feature('Dogs api by https://dog.ceo/api/')
class TestDogsApi:

    @allure.title('Request for a random image of a dog')
    @pytest.mark.smoke
    def test_get_random_dog_image(self):
        """
        Тест проверяет запрос на получение случайного изображения собаки.
        Шаги проверки:
        1. GET запрос на получение объекта с изображением собаки
        2. Проверка статус кода 200
        3. Валидность json
        4. Валидность контента json с определенной моделью
        """
        response = requests.get(Url.RANDOM_IMAGE_URL)
        check_status_code(response, 200)
        response_json = validate_json(response)
        with allure.step('Validate json model'):
            GetResponseDogModel(**response_json)

    @allure.title('Request for a few random photos of dogs')
    @pytest.mark.smoke
    @pytest.mark.parametrize('count_image', [1, 25, 49, 50])
    def test_get_multiply_random_image(self, count_image: int):
        """
        Тест проверяет запрос на получение нескольких случайных фотографий собак.
        Граничные значения для запроса от 1 до 50 (включительно).
        Шаги проверки:
        1. GET запрос на получение объекта со случайным изображением собаки
        2. Проверка статус кода 200
        3. Валидность json
        4. Валидность контента json с определенной моделью
        5. Количество возвращаемых объектов
        """
        response = requests.get(f'{Url.RANDOM_IMAGE_URL}{count_image}')
        check_status_code(response, 200)
        response_json = validate_json(response)
        with allure.step('Validate json model'):
            dog_list = GetResponseListDogModel(**response_json)
        with allure.step('Assertion count of objects'):
            assert len(dog_list.message) == count_image

    @allure.title('Request for all photos of hound dogs')
    @pytest.mark.smoke
    def test_get_images_by_breed_hound(self):
        """
        Тест проверяет запрос на получение всех фотографий собак породы hound.
        Шаги проверки:
        1. GET запрос на получение всех фотографий собак породы hound
        2. Проверка статус кода 200
        3. Валидность json
        4. Валидность контента json с определенной моделью
        5. Количество возвращаемых объектов
        """
        response = requests.get(Url.BY_BREED_HOUND_URL)
        check_status_code(response, 200)
        response_json = validate_json(response)
        with allure.step('Validate json model'):
            dog_list = GetResponseListDogModel(**response_json)
        with allure.step('Assertion count of objects'):
            assert len(dog_list.message) == 808

    @allure.title('Request for a list of all dog breeds')
    @pytest.mark.smoke
    def test_get_list_all_breeds(self):
        """
        Тест проверяет запрос на получение списка всех пород собак.
        Шаги проверки:
        1. GET запрос на получение списка всех пород собак
        2. Проверка статус кода 200
        3. Валидность json
        4. Валидность контента json с определенной моделью
        5. Количество возвращаемых объектов
        """
        response = requests.get(Url.LIST_ALL_BREEDS_URL)
        check_status_code(response, 200)
        response_json = validate_json(response)
        with allure.step('Validate json model'):
            dog_list = GetResponseListBreedsModel(**response_json)
        with allure.step('Assertion count of objects'):
            assert len(list(dog_list.message)) == 98

    @allure.title('Request for a random photo of a hound dog')
    @pytest.mark.smoke
    def test_get_random_image_from_breed__hound_collection(self):
        """
        Тест проверяет запрос на получение случайной фотографии собаки породы hound
        Шаги проверки:
        1. GET запрос на получение случайной фотографии собаки породы hound
        2. Проверка статус кода 200
        3. Валидность json
        4. Валидность контента json с определенной моделью
        """
        response = requests.get(Url.RANDOM_IMAGE_FROM_BREED_HOUND_URL)
        check_status_code(response, 200)
        response_json = validate_json(response)
        with allure.step('Validate json model'):
            GetResponseDogModel(**response_json)

    @allure.title('Request for several photos of dogs with the hound breed')
    @pytest.mark.smoke
    @pytest.mark.parametrize('count_image', [1, 2, 3],)
    def test_get_multiple_images_from_breed_hound_collection(self, count_image):
        """
        Тест проверяет запрос на получение нескольких фотографий собак с породой hound.
        Шаги проверки:
        1. GET запрос на получение нескольких фотографий собак с породой hound
        2. Проверка статус кода 200
        3. Валидность json
        4. Валидность контента json с определенной моделью
        5. Количество возвращаемых объектов
        """
        response = requests.get(f'{Url.MULTIPLE_IMAGES_FROM_BREED_HOUND_URL}{count_image}')
        check_status_code(response, 200)
        response_json = validate_json(response)
        with allure.step('Validate json model'):
            dog_list = GetResponseListDogModel(**response_json)
        with allure.step('Assertion count of objects'):
            assert len(dog_list.message) == count_image
