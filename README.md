## Хакатон Цифровой прорыв ДФО
# Разработка помощника для создания визуального контента
## Трек: Генерация визуальной поддержки
## **Настройка сервиса**
### Создаем виртуальную среду
```cmd
python -m venv venv
```
### Активируем среду
```cmd
venv\Scripts\activate
```
### Скачиваем библиотеки
```cmd
python -m pip install -r requirements.txt
```
### [Устанавливаем библиотеку GigaChain (для работы с GigaChat API)](https://developers.sber.ru/docs/ru/gigachat/sdk/get-started/quickstart#ustanovka-sertifikatov-mintsifry)
```cmd
pip install gigachain
```
### [Устанавливаем сертификат Минцифры (для работы с GigaChat API)](https://developers.sber.ru/docs/ru/gigachat/sdk/get-started/quickstart#ustanovka-sertifikatov-mintsifry)
1. Установите утилиту gigachain-cli
```cmd
pip install gigachain-cli
```
2. Установите сертификаты 
```cmd
gigachain install-rus-certs
```
### Устанавливаем СУБД Postgresql
### [Скачиваем кодек ffmpeg](https://ffmpeg.org/download.html) и размещаем в папку bin в корне проекта файл .exe для Windows или пакет для UNIX-систем
### Настраиваем переменную среды PATH для утилит управления БД и доступа к драйверу ffmpeg (пример для Windows) 
### %PATH% - дописываем к существующим вначало
```
PATH=C:\Program Files\PostgreSQL\10\bin;D:\MyPrj\iiassistant\bin;%PATH%
```
### Запускаем утилиту psql 
```cmd
psql
```
### Создаем пользователя
```cmd
CREATE USER admin WITH PASSWORD 'admin';
``` 
### Создаем БД с собственником admin
```cmd
CREATE DATABASE admin OWNER admin ENCODING 'UTF8';
\q
```
### Создаем миграции
```cmd
python manage.py makemigrations
```
### Мигрируем (пересоздать БД если не мигрируется)
```cmd
python manage.py migrate
```
### Создаум суперюзера для доступа к административной панели django
```cmd
python manage.py createsuperuser
Username: admin
Password: admin
```
## **Работа с сервисом**
### Переходим в корневую дирректорию проекта и запускаем его (остановка сервера Ctrl+C)
```cmd
python manage.py runserver
```
### Работа с административной панелью 
- переходим по http://79.174.84.28:8000/admin/
- вводим имя: admin, пароль: admin
- видим таблицу с промтами пользователя и (или) транскрибированной речью с микрафона
### Работа с сервисом
- эндпоинт генерации изображения по речи http://79.174.84.28:8000/picasso/api/audio/
- эндпоинт генерации изображения по текстовому промту http://79.174.84.28:8000/picasso/api/text/ 
- эндпоинт сброса истории чата http://79.174.84.28:8000/picasso/api/clear/



