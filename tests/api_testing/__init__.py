import json
import requests
import logging
import allure

logger = logging.getLogger(__name__)


def check_status_code(response: requests, status_code: int) -> None:
    with allure.step('Assertion status code'):
        assert response.status_code == status_code, f'Статус код должен быть {status_code}'


def validate_json(response: requests) -> json:
    with allure.step('JSON validate'):
        try:
            response_json = json.loads(response.content)
            return response_json
        except ValueError as e:
            logger.exception(e)
            raise AssertionError(f"Невалидный JSON, ошибка: {e}")
