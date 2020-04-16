# ТЕСТОВОЕ ЗАДАНИЕ на позицию Junior Backend разработчик 

#### Установка Docker
* [Подробное руководство по установке docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

##### Установка docker-compose

* [Подробное руководство по установке docker-compose](https://docs.docker.com/compose/install/)

## запуск сервиса
сначала скопировать данный репозиторий 

~~~
$ git clone https://github.com/Rimasko/juniorTest.git
$ cd juniorTest
~~~
запустить сборку docker-compose

~~~
$ sudo docker-compose build
~~~

запустить сервис

~~~
$ sudo docker-compose up
~~~


для начала узнаем ID нашего контейнера
imagename = juniortest_server
~~~
$ sudo docker ps
~~~
после необходимо првести миграции в базу данных и собрать статику
~~~
$ sudo docker exec -i (ID) python manage.py makemigrations
$ sudo docker exec -i (ID) python manage.py migrate
$ sudo docker exec -i (ID) python manage.py collectstatic
~~~
теперь по адресу 
http://0.0.0.0:8000/api/deals/ отправим POST запрос с файлом deals.csv
дождемся резуьтата ответа, 
после отправить GET запрос на этот же адрес и получим ответ с полем response 
```json
  "response": [
        {
            "username": "resplendent",
            "spent_money": 451731,
            "gems": [
                "Сапфир",
                "Танзанит",
                "Рубин"
            ]
        },
        {
            "username": "bellwether",
            "spent_money": 217794,
            "gems": [
                "Сапфир",
                "Петерсит"
            ]
        },
        {
            "username": "uvulaperfly117",
            "spent_money": 120419,
            "gems": [
                "Танзанит",
                "Петерсит"
            ]
        },
        {
            "username": "braggadocio",
            "spent_money": 108957,
            "gems": [
                "Изумруд"
            ]
        },
        {
            "username": "turophile",
            "spent_money": 100132,
            "gems": [
                "Рубин",
                "Изумруд"
            ]
        }
    ]
```