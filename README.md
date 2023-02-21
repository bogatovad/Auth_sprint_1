## Ссылка на репозиторий
https://github.com/bogatovad/Auth_sprint_1

Авторы:
 - [bogatovad](https://github.com/bogatovad)
 - [Seniacat](https://github.com/Seniacat)
 - [acetone415](https://github.com/acetone415)


# Сервис аутентификации и авторизации


## Возможности сервиса

- регистрация пользователя;
- вход пользователя в аккаунт (обмен логина и пароля на пару токенов: JWT-access токен и refresh токен); 
- обновление access и refresh токенов;
- выход пользователя из аккаунта;
- изменение логина или пароля;
- получение пользователем своей истории входов в аккаунт;


## Используемые технологии

- Flask
- PostgreSQL
- Redis
- Docker
- Pytest
- SQLAlchemy

## Запуск
Создать и заполнить .env из .env.example в папке `Auth_sprint_1/envs`.
Из этой папки `Auth_sprint_1` выполнить:
```
make start
```

## Запуск тестов

Из контейнера flask (`auth_sprint_1_auth_1`) запустить pytest:
```
docker exec -it auth_sprint_1_auth_1 bash

pytest
```

## Документация API
Доступна по адресу `http://host:port/apidocs`