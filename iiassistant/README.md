# Хакатон MTC_True_Tech
# Создание сервиса виртуального помошника
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
### Загружаем данные из фикстуры iiassistat_data.json в БД
```cmd
python manage.py loaddata iiassistant_data.json
```
### Если фикстуры не занрузятся очистить БД и снова повторить миграции.
```cmd
python manage.py flush
```
### Создаум суперюзера для доступа к административной панели django
```cmd
python manage.py createsuperuser
Username: admin
Password: admin
```
### Настраиваем Поиск по триграммному сходству, переходим в  нашу БД admin
```cmd
psql admin
```
### Устанавливаем расширение postgresql для созданной БД
```cmd
CREATE EXTENSION pg_trgm;
```
### Проверяем установленные расширения (при необходимости)
```cmd
SELECT * FROM pg_extension WHERE extname = 'pg_trgm';
\q
```
## **Работа с сервисом**
### Переходим в корневую дирректорию проекта и запускаем его (остановка сервера Ctrl+C)
```cmd
python manage.py runserver
```
### Работа с административной панелью 
- переходим по http://127.0.0.1:8000/admin/
- вводим имя: admin, пароль: admin
- видим таблицу с командами и таблицу с транскрибированной речью с микрафона
### Работа с сервисом
- переходим по http://127.0.0.1:8000/transcription/record-audio/
- жмем запись и разрешаем запись с микрафона 
- произносим запрос и останавливаем запись



