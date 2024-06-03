from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status

from picasso.models import UsersPromts
from picasso.serializers import AudioFileSerializer, UsersPromtsSerializer
from rest_framework.views import APIView
# from django.shortcuts import get_object_or_404
# from django.core.serializers.json import DjangoJSONEncoder

import os
import subprocess
from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment

# Create your views here.

# Установка сертификатов минцифры
# https://developers.sber.ru/docs/ru/gigachat/sdk/get-started/quickstart#ustanovka-sertifikatov-mintsifry

client_id = '0987f8e1-23f0-4dca-b9d9-fea9cf05af7c'
secret = '726900f1-64b6-4fb9-afdd-8a6a4d960447'
# Данные авторизации пользователя
auth = 'MDk4N2Y4ZTEtMjNmMC00ZGNhLWI5ZDktZmVhOWNmMDVhZjdjOjcyNjkwMGYxLTY0YjYtNGZiOS1hZmRkLThhNmE0ZDk2MDQ0Nw=='

import requests
import uuid # Библиотека для генерации RqUID
import json
import shutil

from bs4 import BeautifulSoup
from datetime import datetime


# Запускаем запись звука record_audio.html 
def record_audio(request):
    return render(request, 'sound.html')

# Эндпоинт для обработки audioBlob (команды в функции)
class AudioView(APIView):
    
    def post(self, request):
        serializer = AudioFileSerializer(data=request.FILES)
        if serializer.is_valid():
            audio_file = serializer.validated_data['audio']
            # Сохранение аудиофайла в папке media
            media_path = os.path.join(settings.MEDIA_ROOT, audio_file.name)
            audio_segment = AudioSegment.from_file(audio_file)
            audio_file_mp3 = audio_segment.export(media_path, format="mp3") 
            
            # Выполняем функцию транскрибации
            convert_text = sound_in_text(audio_file_mp3) 
            
            # Генерируем токен
            token = get_token(auth)
            
            # Подключаем диалоговую систему
            # Получаем данные из кэша
            next_text = load_chat_history_from_file('completions_history.json')
            # print(next_text)
            
            if next_text == None:
              # Первичный запрос пользователя
              img_id = get_chat_completions(token, convert_text)
              print('ПЕРВИЧНЫЙ')
              
            else:  
              # Последующие запросы пользователя
              img_id = get_chat_completions_updated(token, next_text, convert_text)
              print('ПОСЛЕДУЮЩИЙ')    
              
            # Завариваем суп и ищем src сгенерированной картинки
            soup = BeautifulSoup(img_id['content'], 'html.parser')
            # soup = BeautifulSoup(img_id, 'html.parser')
            try:
              img_src = soup.img['src']
            except:
              img_src = 'Создайте правильный запрос согласно правил https://developers.sber.ru/help/gigachat/how-to-generate-images'
            
            # Отдаем на фронт текст пользователя и src картинки
            content = handle_command(convert_text, img_src)
            
            # Сохраняем картинку по id на бэке (это нужно реализовать на фронте)
            now = datetime.now()
            dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
            get_chat_content(token, img_src, str(dt_string))
            return Response(content, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        '''Метод принимающий на вход и запросы GET'''
        weaponts = UsersPromts.objects.all()
        ser = UsersPromtsSerializer(weaponts, many=True)
        return Response(ser.data)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class TextView(APIView):
    
    def post(self, request):
      '''
      Тестовый post-запрос
      {
      "usertext": "Нарисуй кота, он играет в компьютерную игру, дом, вокруг еда, эффект тёплого света, мультяшный стиль."
      }
      '''
      serializer = UsersPromtsSerializer(data=request.data)
      if serializer.is_valid():
          serializer.save()
          # Получаем валидный промт из сериализатора
          convert_text = serializer.validated_data['usertext']

          # Генерируем токен
          token = get_token(auth)
          
          # Подключаем диалоговую систему
          # Получаем данные из кэша
          next_text = load_chat_history_from_file('completions_history.json')
          # print(next_text)
          
          if next_text == None:
            # Первичный запрос пользователя
            img_id = get_chat_completions(token, convert_text)
            print('ПЕРВИЧНЫЙ')
            
          else:  
            # Последующие запросы пользователя
            img_id = get_chat_completions_updated(token, next_text, convert_text)
            print('ПОСЛЕДУЮЩИЙ')    
            
          # Завариваем суп и ищем src сгенерированной картинки
          soup = BeautifulSoup(img_id['content'], 'html.parser')
          # soup = BeautifulSoup(img_id, 'html.parser')
          try:
            img_src = soup.img['src']
          except:
            img_src = 'Создайте правильный запрос согласно правил https://developers.sber.ru/help/gigachat/how-to-generate-images'
          
          # Отдаем на фронт текст пользователя и src картинки
          content = handle_command(convert_text, img_src)
          
          # Сохраняем картинку по id на бэке (это нужно реализовать на фронте)
          now = datetime.now()
          dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
          get_chat_content(token, img_src, str(dt_string))
          return Response(content, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        '''Метод принимающий на вход и запросы GET'''
        weaponts = UsersPromts.objects.all()
        ser = UsersPromtsSerializer(weaponts, many=True)
        return Response(ser.data)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class ClearView(APIView):
  def post(self, request):
    clear_file_content('completions_history.json')
    return Response(status=status.HTTP_200_OK)
  
  def get(self, request):
      return Response(status=status.HTTP_200_OK)
  
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Отдаем на фронт текст пользователя и src картинки
def handle_command(user_text, image_id):
    context = {} # Словарь используемый для ответа на POST-запрос на фронт
    context['convert_text'] = user_text
    context['img_text'] = f'Вот ссылка на сгенерированное изображение: {image_id}'
    return context

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Транскрибация
def sound_in_text(audio_file_mp3):
    '''
    Функция транскрибации
    audio_file_mp3 - аудиофайл формата .mp3 
    '''
    
    SetLogLevel(0)  # Логирование

    # Задаем путь к статике и медиа
    static_path = os.path.join(settings.STATICFILES_DIRS[0])
    media_path = os.path.join(settings.MEDIA_ROOT)

    # Проверяем наличие модели в текущей рабочей директории
    if not os.path.exists(static_path + "/speech/model"):
        print("Пожалуйста, загрузите модель с https://alphacephei.com/vosk/models и разархивируйте как 'model' в текущей папке.")
        # преждевременное завершение программы из-за отсутствия модели, необходимой для работы дальнейших инструкций.
        exit(1)

    # Устанавливаем Frame Rate
    FRAME_RATE = 16000
    CHANNELS = 1

    model = Model(static_path + "/speech/model")
    rec = KaldiRecognizer(model, FRAME_RATE)
    rec.SetWords(True)

    # Используя библиотеку pydub делаем предобработку аудио
    mp3 = AudioSegment.from_mp3(media_path + '/recorded_audio.mp3')
    mp3 = mp3.set_channels(CHANNELS)
    mp3 = mp3.set_frame_rate(FRAME_RATE)

    rec.AcceptWaveform(mp3.raw_data)
    result = rec.Result()
    # Декодируем вывод строки json "{\n  \"text\" : \"\"\n}" в словарь Python
    text = json.loads(result)['text']
    # сохраняем в модель UsersPromts БД в поле usertext
    UsersPromts.objects.create(usertext=text) 
    
    return text

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Генерируем токен
def get_token(user_auth):
    '''
    Функция генерации токена
    user_auth - данные авторизации пользователя
    '''
    rq_uid = str(uuid.uuid4())
    
    # эндпоинт GigaChat для генерации токена
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload='scope=GIGACHAT_API_PERS'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': rq_uid,
    'Authorization': f'Basic {user_auth}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    token = response.json()["access_token"]
    # print(token)
    return token

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Скачиваем изображение
def get_chat_content(user_token, image_id, path):

  # эндпоинт GigaChat для скачивания сгенерированного изображения по image_id
  url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{image_id}/content"

  headers = {
    'Accept': 'application/jpg',
    'Authorization': f'Bearer {user_token}'
  }

  response = requests.request("GET", url, headers=headers, stream=True)

  with open(f'{path}.jpg', 'wb') as out_file:
      shutil.copyfileobj(response.raw, out_file)
  del response

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Обрабатываем первичный запрос пользователя
def get_chat_completions(user_token, user_message):
    
  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat",
    "messages": [
      {
        "role": "user", 
        # системная роль - устанавливает кем будет считать себя нейросеть ГигаЧат
        # пользовательская роль - это человек взаимодействующий с ГигаЧатом
        # роль ассистента - ответ от ГигаЧата
        "content": user_message
      }
    ],
    "temperature": 1, # Температура генерации (0 - самый подходящий ответ, 1 - более случайный ответ)
    # - определяет насколько случайный ответ будет в генерации
    "top_p": 0.1, # Контроль разнообразия ответов
    "n": 1, # Количество возвращаемых ответов
    "stream": False, # Потоковая передачи результатов генерации (печатает побуквенно)
    "max_tokens": 512, # 1 токен = 3-4 символа
    "repetition_penalty": 1, # Штраф за повторение
    "function_call": "auto" # ГигаЧат может обрабатывать наши функции, но 
    # функция Кандинского выбирается автоматически в зависимости от промта
  })
  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {user_token}'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  content = response.json()["choices"][0]["message"]
  # content = response.json()["choices"][0]["message"]["content"] # + ', '
  # content = response.json()
  # Сохраняем ответ нейронки в кэш
  save_chat_history_to_file(content, 'completions_history.json')

  return content

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Обрабатываем последующие запросы пользователя
def get_chat_completions_updated(user_token, preview_content, user_updated_message):

  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  msg = []
  msg.insert(0, preview_content) # предыдущий запрос-ответ
  msg.insert(1, {"role": "user", "content": user_updated_message}) # уточняющий запрос-ответ
  
  print(msg)
  payload = json.dumps({
    "model": "GigaChat",
    "messages": msg, # список с предыдущими запросами и ответами и уточняющим запросом
    "temperature": 0.1, # изменено для менее случайных изменений предыдущей генерации
    "top_p": 1, # для тех же целей увеличено но степень влияния нужно дополнительно проверять
    "n": 1,
    "stream": False,
    "max_tokens": 512,
    "repetition_penalty": 1,
    "function_call": "auto"
  })
  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {user_token}'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  
  content = response.json()["choices"][0]["message"]
  # content = response.json()["choices"][0]["message"]["content"]
  # content = response.json()
  # Сохраняем ответ нейронки в кэш
  save_chat_history_to_file(content, 'completions_history.json')

  msg.clear() 
  print(msg)
  
  return content

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Сохраняем ответ нейронки в кэш
def save_chat_history_to_file(completions_history, path_cashe):
    with open(path_cashe, 'w') as file:
        json.dump(completions_history, file)
import json

def load_chat_history_from_file(path_cache):
    try:
        with open(path_cache, 'r') as file:
            completions_history = json.load(file)
            # print(completions_history)
            return completions_history
    except json.JSONDecodeError as e:
        # print(f"Error loading JSON: {e}")
        return None

# Очищаем ответ нейронки 
def clear_file_content(path_cache):
    with open(path_cache, 'w') as file:
        file.truncate(0)
