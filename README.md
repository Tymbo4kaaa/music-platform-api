Music Platform API

Backend API для музыкальной стриминговой платформы (аналог Spotify, Яндекс музыки и т.д), написанный на "Django REST Framework".

Описание
Проект предоставляет RESTful API для управления музыкальным контентом: жанрами, исполнителями, альбомами и треками. Реализована система аутентификации через JWT-токены, возможность создания плейлистов, лайкания треков и фильтрации контента.

Что использовалось
- Python 3.12
- Django 5.2
- Django REST Framework 3.17
- SimpleJWT -аутентификация
- drf-spectacular-автоматическая документация (Swagger)
- SQLite(для разработки)

Функционал

- Регистрация и авторизация пользователей (JWT)
- CRUD операции для жанров, исполнителей, альбомов, треков
-Управление плейлистами (создание, добавление/удаление треков)
-Система лайков (toggle)
- Фильтрация и поиск (по названию, артисту, жанру, длительности)
- Счетчик прослушиваний (автоматический инкремент при просмотре)

Установка
1. Клонируйте репозиторий:
   bash
   git clone URL_ЕПОЗИТОРИЯ
cd music-platform-api
2.
Создайте виртуальное окружение и активируйте его:
python -m venv venv
# PowerShell:
.\venv\Scripts\Activate.ps1
# Git Bash:
source venv/Scripts/activate
3.
Установите зависимости:
pip install -r requirements.txt
4.
Примените миграции:
python manage.py migrate
5.
Создайте суперпользователя:
python manage.py createsuperuser
6.
Запустите сервер:
python manage.py runserver

По этому url заходим 
http://127.0.0.1:8000/api/v1/
Аутентификация
POST  /api/token/          Получить access и refresh токены
POST  /api/token/refresh/  Обновить access токен
Музыкальные сущности
GET/POST       /genres/              Список и создание жанров
GET/POST       /artists/             Список и создание исполнителей
GET/POST       /albums/              Список и создание альбомов
GET/POST       /tracks/              Список и создание треков
POST/DELETE    /tracks/{id}/like/    Поставить/снять лайк

Плейлисты
GET/POST  /playlists/                         Список и создание плейлистов
POST      /playlists/{id}/add-track/          Добавить трек в плейлист
DELETE    /playlists/{id}/remove-track/       Удалить трек из плейлиста