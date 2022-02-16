# Тестовое задание для ЛИИС

Веб-сервер предоставляет API, позволяющий формировать ленту статей для пользователй.

Доступные методы:

```
/api/
    register/
        post:
            description: Регистрация пользователя
    article/
            get:
                description: Выдать список всех доступных статей
            post:
                description: Добавить статью
            /{articleId}
                    get:
                        description: Выдать статью по id
                    put:
                        descriiption: Изменить статью
```
