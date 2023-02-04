## Сервис расписаний междугороднего транспорта.

### deployment

Заполнить API_KEY в файле .ENV

```
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

```


Открыть  localhost  с параметрами  http://127.0.0.1:8000/<широта>-<долгота>

Например с координатами краснодара  ```http://127.0.0.1:8000/45.039268-38.987221```
