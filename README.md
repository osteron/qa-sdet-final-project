# Проектная работа
Проектная работа содержит в себе две части - тестирование API-сервисов и тестирование UI Opencart.

## Предварительные условия
- Установлен python версии не ниже 3.11
- Установлен docker версии не ниже 24.0.6
- Установлен docker-compose версии не ниже 1.29.2
- Установлен allure версии не ниже 2.24.1

## Общее
После запуска тестов автоматически создается директория <i>allure-results</i> 
в корне проекта с результатами работы автотестов. 

### Просмотр отчетов Allure
Выполнить команду в корне директории:
```shell
allure serve allure-results
```

## Установка
1. Клонировать репозиторий
```shell
git clone https://github.com/osteron/qa-sdet-final-project.git
```
2. Создать виртуальное окружение venv 
```shell
python3 -m venv venv
```
3. Активировать виртуальное окружение
   - Windows
    ```shell
    venv\Scripts\activate.bat
    ```
   - Unix
    ```shell
    source venv/bin/activate
    ```
4. Установить необходимые пакеты
```shell
pip install -r requirements.txt
```

## 1. Тестирование API
### 1.1 Описание

В проектной работе содержатся три директории с автотестами по пути `test/api_testing` для трех разных сервисов:
- `dog_api`
- `jsonplaceholder`
- `openbrewerydb`

Данные автотесты были разработаны согласно домашних заданий по разработке API-тестов.


### 1.2 Запуск автотестов

Для локального запуска:
- всех API-тестов используется команда:
```shell
pytest -n 2 tests/api_testing/
```

- API-тестов для конкретных сервисов используются команды:
```shell
pytest -n 2 tests/api_testing/dog_api
```
```shell
pytest -n 2 tests/api_testing/jsonplaceholder
```
```shell 
pytest -n 2 tests/api_testing/openbrewerydb
```

где `n` - количество параллельно выполняемых тестов.

## 2. Тестирование UI Opencart
### 2.1 Описание
В проектной работе содержатся две директории, связанные с тестированием UI Opencart:
- `page_objects`: страницы opencart
- `tests/ui_testing`: UI автотесты opencart

Предварительно необходимо запустить проект Opencart.

### 2.2 Запуск и остановка проекта Opencart
Для запуска проекта Opencart необходимо в корне директории воспользоваться командой терминала:
```shell
OPENCART_PORT=8081 PHPADMIN_PORT=8888 LOCAL_IP=192.168.1.33 docker-compose up -d
```

где `LOCAL_IP` - IP адрес локальной машины, на котором происходит запуск проекта Opencart.

Для остановки проекта Opencart необходимо в корне директории воспользоваться командой терминала:
```shell
OPENCART_PORT=8081 PHPADMIN_PORT=8888 LOCAL_IP=192.168.1.33 docker-compose down
```

### 2.3 Запуск автотестов
#### 2.3.1 Используемые флаги
Для запуска UI автотестов необходимо использовать следующие флаги:
- `--browser [chrome, firefox]`: используемый браузер для запуска тестов (по умолчанию `chrome`)
- `--bv`: версия браузера (по умолчанию `117.0`)
- `--url`: url адрес проекта Opencart (по умолчанию `http://localhost:8081`)
- `--executor`: локальное или удаленное выполнение тестов (по умолчанию `local`, для удаленного запуска 
необходимо ввести ip адрес selenoid хаба)
- `--vnc`: включение и отключение функции vnc (по умолчанию `False`)
- `--logs`: включение и отключение сохранения логов (по умолчанию `False`)
- `-n`: количество параллельно выполняемых тестов
#### 2.3.2 Запуск автотестов локально
Для запуска UI автотестов локально можно воспользоваться командой:
```shell
pytest -n 2 tests/ui_testing --url http://192.168.1.33:8081
```

Если необходимо запустить отдельный test suite, можно воспользоваться следующей командой:
```shell
pytest -n 2 tests/ui_testing/test_catalog.py --url http://192.168.1.33:8081
```

#### 2.3.3 Запуск автотестов с помощью Selenoid
Для запуска UI автотестов удаленно (в данном примере - selenoid hub на localhost) можно воспользоваться командой:
```shell
pytest -n 2 tests/ui_testing --executor localhost --url http://192.168.1.33:8081
```
