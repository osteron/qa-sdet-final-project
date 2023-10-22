import allure
import pytest
import requests
from .urls import Url
from .models import GetResponseBreweryModel, GetResponseListBreweryModel, GetResponseAutocompleteModel
from .. import validate_json, check_status_code


@allure.feature('API testing by https://api.openbrewerydb.org')
class TestBreweryApi:

    @allure.title('Request for a list of breweries')
    @pytest.mark.smoke
    @pytest.mark.parametrize('params, count_brewery', [
        ('', 50),
        ('per_page=1', 1),
        ('per_page=5', 5),
        ('per_page=0', 0),
    ])
    def test_get_list_breweries(self, params: str, count_brewery: int) -> None:
        """
        Тест проверяет запрос на получение списка пивоваренных заводов.
        Шаги проверки:
        1. GET запрос с параметрами
        2. Проверка статус кода 200
        3. Валидность json
        4. Валидность контента json с определенной моделью
        5. Проверка длины списка - количество пивоваренных заводов
        """
        response = requests.get(Url.BASE_URL, params=params)
        check_status_code(response, 200)
        response_json = validate_json(response)
        with allure.step('Validate json model'):
            brewery_list = GetResponseListBreweryModel(RootModel=response_json)
        with allure.step('Assertion count of brewery'):
            assert len(brewery_list.RootModel) == count_brewery

    @allure.title('Request for a list of breweries with a selection by city')
    @pytest.mark.smoke
    @pytest.mark.parametrize('params, city, count_brewery', [
        ('by_city=san_diego&per_page=50', 'san diego', 50),
        ('by_city=norman&per_page=3', 'norman', 3),
        ('by_city=austin&per_page=15', 'austin', 15)
    ])
    def test_get_list_breweries_by_city(self, params: str, count_brewery: int, city: str) -> None:
        """
        Тест проверяет запрос на получение списка пивоваренных заводов с выборкой по городу.
        Шаги проверки:
        1. GET запрос с параметрами
        2. Проверка статус кода 200
        3. Валидность json
        4. Проверка длины списка - количество пивоваренных заводов
        5. Цикл с перебором элементов списка json:
            5.1 проверка каждого элемента списка на валидность json с определенной моделью
            5.2 проверка на наличие названия заданного города в теле json
        """
        response = requests.get(Url.BASE_URL, params=params)
        check_status_code(response, 200)
        response_json = validate_json(response)
        with allure.step('Assertion count of brewery'):
            assert len(response_json) == count_brewery
        with allure.step('Validate json model'):
            models = [GetResponseBreweryModel(**model) for model in response_json]
        with allure.step('Assertions availability of cities in response'):
            for model in models:
                assert city in model.city.lower()

    @allure.title('Request to get a brewery by its id')
    @pytest.mark.smoke
    @pytest.mark.parametrize('brewery_id', ['b54b16e1-ac3b-4bff-a11f-f7ae9ddc27e0'])
    def test_get_single_brewery(self, brewery_id: str) -> None:
        """
        Тест проверяет запрос на получение пивоваренного завода по его id.
        Шаги проверки:
        1. GET запрос на получение объекта пивоваренного завода по его id
        2. Проверка статус кода 200
        3. Валидность json
        4. Валидность контента json с определенной моделью
        5. Проверка наличия заданного id в теле контента json.id
        """
        response = requests.get(f'{Url.BASE_URL}{brewery_id}')
        check_status_code(response, 200)
        response_json = validate_json(response)
        with allure.step('Validate json model'):
            brewery = GetResponseBreweryModel(**response_json)
        with allure.step('Assertion brewery id'):
            assert brewery.id == brewery_id

    @allure.title('Request to get a list of breweries with the specified size')
    @pytest.mark.smoke
    @pytest.mark.parametrize('params, count_brewery', [('size=3', 3), ('size=10', 10), ('', 1), ('size=50', 50)])
    def test_get_random_brewery_with_size(self, params: str, count_brewery: int) -> None:
        """
        Тест проверяет запрос на получение списка пивоваренных заводов с заданных size (количество).
        Шаги проверки:
        1. GET запрос с параметрами на получение списка пивоваренных заводов
        2. Проверка статус кода 200
        3. Валидность json
        4. Валидность контента json с определенной моделью
        5. Проверка длины списка - количество пивоваренных заводов
        """
        response = requests.get(Url.RANDOM_BREWERY_URL, params=params)
        check_status_code(response, 200)
        response_json = validate_json(response)
        with allure.step('Validate json model'):
            brewery_list = GetResponseListBreweryModel(RootModel=response_json)
        with allure.step('Assertion count of brewery'):
            assert len(brewery_list.RootModel) == count_brewery

    @allure.title('Request for a list of breweries with a word search')
    @pytest.mark.smoke
    @pytest.mark.parametrize('params, word_search, count_brewery', [
        ('query=dog', 'dog', 15),
        pytest.param('query=austin', 'austin', 53, marks=pytest.mark.skip(reason='don\'t fix bug with search by word')),
        pytest.param('query=diego', 'diego', 53, marks=pytest.mark.skip(reason='don\'t fix bug with search by word'))])
    def test_get_autocomplete_with_query(self, params: str, word_search: str, count_brewery: int) -> None:
        """
        Тест проверяет запрос на получение списка пивоваренных заводов с поиском по слову.
        Шаги проверки:
        1. GET запрос с параметрами на получение списка пивоваренных заводов
        2. Проверка статус кода 200
        3. Валидность json
        4. Проверка длины списка - количество пивоваренных заводов
        5. Цикл с перебором элементов списка json:
            5.1 проверка каждого элемента списка на валидность json с определенной моделью
            5.2 проверка на наличие искомого слова в теле json.name
        """
        response = requests.get(Url.AUTOCOMPLETE_URL, params=params)
        check_status_code(response, 200)
        response_json = validate_json(response)
        with allure.step('Assertion count of brewery'):
            assert len(response_json) == count_brewery
        with allure.step('Validate json model'):
            for models in response_json:
                query_result = GetResponseAutocompleteModel(**models)
                with allure.step('Assertion word search in query result'):
                    assert word_search in query_result.name.lower()
