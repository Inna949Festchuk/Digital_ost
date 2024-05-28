from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status

from picasso.models import UsersPromts
from picasso.serializers import AudioFileSerializer, UsersPromtsSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

import os
import subprocess
from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment

# Create your views here.

client_id = '0987f8e1-23f0-4dca-b9d9-fea9cf05af7c'
secret = '726900f1-64b6-4fb9-afdd-8a6a4d960447'
# Данные авторизации пользователя
auth = 'MDk4N2Y4ZTEtMjNmMC00ZGNhLWI5ZDktZmVhOWNmMDVhZjdjOjcyNjkwMGYxLTY0YjYtNGZiOS1hZmRkLThhNmE0ZDk2MDQ0Nw=='

import requests
import uuid # Библиотека для генерации RqUID
import json
import shutil

# from bs4 import BeautifulSoup


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
            content = handle_command(convert_text)
            print(convert_text)            
            print(content)
                            
            return Response(content, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def handle_command(convert_text):
    context = {} # Словарь используемый для ответа на POST-запрос
    context['convert_text'] = convert_text
    context['img_text'] = 'Вот ссылка на сгенерированное изображение'
    return context

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Транскрибация
def sound_in_text(audio_file_mp3):
    '''
    Функция транскрибации
    audio_file_mp3 - аудиофайл формата .mp3

    Дополнительно установить ffmpeg (менеджер pip не всегда срабатывает)
    при установке в конду использовать conda install -c conda-forge ffmpeg
    или скачать отдельно с сайта https://ffmpeg.org/download.html пакеты кодека ffmpeg
    Установите переменные среды с помощью путей к двоичным файлам FFmpeg:
    В Windows запустите:
    SET PATH=D:\path\to\transcription\bin;%PATH%
    В Unix или MacOS запустите:
    export FFMPEG_PATH=/path/to/ffmpeg:
    Открытые модели для распознавания русской речи:
    https://alphacephei.com/nsh/2023/01/15/russian-models.html
    поместить в папку picasso/static/speech/ 
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

# token = get_token(auth)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Скачиваем изображение
# Для скачивания изображения передайте полученный идентификатор в запросе GET /files/{file_id}/content:

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

  print('OK!')

# img_id = "a095edc7-37ae-4814-9bd1-c33a890ce050"
# my_path = 'gen1'
# get_chat_content(token, img_id, my_path)


#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Делаем диалоговую систему
def get_chat_completions_history(user_token, user_message, conversation_history=[]):
  '''
  https://developers.sber.ru/docs/ru/gigachat/api/images-generation?lang=py
  Генерация текста/ Изображений (модель по промту пользователя сама понимает, что ей нужно подключить кондинского)

  ГЕНЕРИРУЙ ПРОМТЫ ПО МЕТОДИКЕ СБЕРА ПРАВИЛЬНО!!!!!!!!!!!!!
  1) Как формулировать запросы к GigaChat
  https://developers.sber.ru/help/gigachat/prompt-guide
  2) Генерация изображений по описанию
  https://developers.sber.ru/help/gigachat/how-to-generate-images

  Пример правильного промта:
  Нарисуй кота, он играет в компьютерную игру, дом, вокруг еда, эффект тёплого света, мультяшный стиль.

  | Основной |  Обстановка  | Место | Другие детали | Стиль
  | объект   |              |       |               |
  |          | Он играет в  |       | Вокруг еда,   | Мультяшный
  |   Кот    | компьютерную |  Дом  | эффект        | стиль
  |          | игру         |       | теплого света |
  |          |              |       |               |

  '''

  # эндпоинт GigaChat для генерации текста и изображений 
  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  # Если история диалога не предоставлена, инициализируем пустым списком
  if conversation_history is None:
    conversation_history = []

  conversation_history.append({
    "role": "user", # ?подумай может здесь включить системную роль и сразу сказать сети, что ты художник?
    "content": user_message
  })

  payload = json.dumps({
    "model": "GigaChat:latest",
    "messages": conversation_history,
    "temperature": 0.1, # Температура генерации (0 - самый подходящий ответ, 1 - более случайный ответ)
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

  # Добавим ответ модели в историю диалога
  conversation_history.append(response.json()['choices'][0]['message'])

  return conversation_history


# user_msg = "Лошадь пони в стиле цветочного сюрреализма на лугу,  вдохновленный природой камуфляж, цветочный панк, нежные материалы, яркая, студийная фотография. Стиль: Детальное фото."

# response_img = get_chat_completions_history(token, user_msg)

# # soup = BeautifulSoup(response_img[1]['content'], 'html.parser')

# # img_src = soup.img['src']

# # get_chat_content(token, img_src, "gen1")

# print(response_img)

# user_msg = "Дорисуй ей крылья ангела"

# response_img = get_chat_completions_history(token, user_msg)

# print(response_img)

# # user_msg = "Нарисуй вместо яблок бананы"

# # response_img = get_chat_completions_history(token, user_msg)

# # print(response_img)

# # get_chat_content(token, "01916c5e-a74d-44ae-9cb2-d1dd3b528caa", "gen1")
# # get_chat_content(token, "080529e3-27e2-4579-ac9f-9e8a41aab333", "gen2")
# # get_chat_content(token, "49da4e28-2607-425e-a8a2-e26c33c080c8", "gen3")
