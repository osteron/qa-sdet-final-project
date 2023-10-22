import allure
import pytest
import requests
from .models import GetResponseResourceModel, GetResponseResourceListModel
from .urls import Urls
from .. import validate_json, check_status_code

POST_CREATING_RESOURCE = {
    'title': 'foo',
    'body': 'bar',
    'userId': 1,
}

PUT_UPDATING_RESOURCE = {
    'id': 1,
    'title': 'some_title',
    'body': 'some_body',
    'userId': 1,
}


@allure.feature('Api test by https://jsonplaceholder.typicode.com')
class TestResourceApi:

    @allure.title('Get resource by id')
    @pytest.mark.smoke
    @pytest.mark.parametrize('resource_id', [1, 5, 10])
    def test_get_resource(self, resource_id: int) -> None:
        response = requests.get(f'{Urls.BASE_URL}{resource_id}')
        check_status_code(response, 200)
        response_json = validate_json(response)
        with allure.step('Validate json model'):
            resource = GetResponseResourceModel(**response_json)
        with allure.step('Assertion resource id'):
            assert resource.id == resource_id

    @allure.title('Get all resources')
    @pytest.mark.smoke
    def test_get_all_resources(self) -> None:
        response = requests.get(Urls.BASE_URL)
        check_status_code(response, 200)
        response_json = validate_json(response)
        with allure.step('Validate json model'):
            all_resources = GetResponseResourceListModel(RootModel=response_json)
        with allure.step('Assertion count of all resources'):
            assert len(all_resources.RootModel) == 100

    @allure.title('POST request for creating a resource')
    @pytest.mark.smoke
    @pytest.mark.parametrize('post_data', [POST_CREATING_RESOURCE])
    def test_post_creating_resource(self, post_data: dict) -> None:
        response = requests.post(Urls.BASE_URL, json=post_data)
        check_status_code(response, 201)
        response_json = validate_json(response)
        with allure.step('Validate json model'):
            resource = GetResponseResourceModel(**response_json)
        with allure.step('Assertion ID resource'):
            assert resource.id == 101

    @allure.title('PUT request for updating a resource')
    @pytest.mark.smoke
    @pytest.mark.parametrize('put_data, resource_id', [(PUT_UPDATING_RESOURCE, 1)])
    def test_put_updating_resource(self, put_data: dict, resource_id: int) -> None:
        response = requests.put(f'{Urls.BASE_URL}{resource_id}', json=put_data)
        check_status_code(response, 200)
        response_json = validate_json(response)
        with allure.step('Assertion response with request'):
            assert response_json == PUT_UPDATING_RESOURCE

    @allure.title('PATCH request for updating a resource')
    @pytest.mark.smoke
    @pytest.mark.parametrize('patch_data, resource_title, resource_id',
                             [
                                 ({'title': 'qwerty'}, 'qwerty', 1),
                                 ({'title': '!@#%$^'}, '!@#%$^', 2)],
                             ids=['string title', 'symbolic title'])
    def test_patch_update_resource(self, patch_data: dict, resource_title: str, resource_id: int) -> None:
        response = requests.patch(f'{Urls.BASE_URL}{resource_id}', json=patch_data)
        check_status_code(response, 200)
        response_json = validate_json(response)
        with allure.step('Validate json model'):
            resource = GetResponseResourceModel(**response_json)
        with allure.step('Assertion resource title and id'):
            assert resource.title in resource_title
            assert resource.id == resource_id
