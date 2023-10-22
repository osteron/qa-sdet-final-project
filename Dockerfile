FROM heybit/python3.11.0-alpine
WORKDIR /app

COPY requirements.txt .

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["pytest", "tests/api_testing"]