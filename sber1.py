client_id = '0987f8e1-23f0-4dca-b9d9-fea9cf05af7c'
secret = '726900f1-64b6-4fb9-afdd-8a6a4d960447'
auth = 'MDk4N2Y4ZTEtMjNmMC00ZGNhLWI5ZDktZmVhOWNmMDVhZjdjOjcyNjkwMGYxLTY0YjYtNGZiOS1hZmRkLThhNmE0ZDk2MDQ0Nw=='

import requests
import uuid # Библиотека для генерации RqUID
import json
import shutil

from bs4 import BeautifulSoup

rq_uid = str(uuid.uuid4())

url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

payload='scope=GIGACHAT_API_PERS'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json',
  'RqUID': rq_uid,
  'Authorization': f'Basic {auth}'
}

response = requests.request("POST", url, headers=headers, data=payload)
token = response.json()["access_token"]
# print(token)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# ТЕСТ
# # Получаем список моделей

# url = "https://gigachat.devices.sberbank.ru/api/v1/models"

# payload={}
# headers = {
#   'Accept': 'application/json',
#   'Authorization': f'Bearer {token}'
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# ШАГ_1
# https://developers.sber.ru/docs/ru/gigachat/api/images-generation?lang=py
# Генерация текста/ Изображений (модель по промту пользователя сама понимает, что ей нужно подключить кондинского)

# ГЕНЕРИРУЙ ПРОМТЫ ПО МЕТОДИКЕ СБЕРА ПРАВИЛЬНО!!!!!!!!!!!!!
# 1) Как формулировать запросы к GigaChat
# https://developers.sber.ru/help/gigachat/prompt-guide
# 2) Генерация изображений по описанию
# https://developers.sber.ru/help/gigachat/how-to-generate-images

# Пример правильного промта:
# Нарисуй кота, он играет в компьютерную игру, дом, вокруг еда, эффект тёплого света, мультяшный стиль.

# | Основной |  Обстановка  | Место | Другие детали | Стиль
# | объект   |              |       |               |
# |          | Он играет в  |       | Вокруг еда,   | Мультяшный
# |   Кот    | компьютерную |  Дом  | эффект        | стиль
# |          | игру         |       | теплого света |
# |          |              |       |               |

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

  # content_text = response.json()["choices"][0]["message"]["content"]

  content = response.json()

  return content

user_msg = "Нарисуй город с небоскребами, город в космосе, вокруг планеты, эффект киберпанк, корпоративный стиль банка Сбербанк."
# content_response = get_chat_completions(token, user_msg)

# print(content_response)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Ответ на промт "Привет! Как дела?"
# {'choices': [{'message': {'content': 'Привет! У меня всё отлично, а как дела у тебя?', 'role': 'assistant'}, 'index': 0, 'finish_reason': 'stop'}], 'created': 1716577782, 'model': 'GigaChat:3.1.25.3', 'object': 'chat.completion', 'usage': {'prompt_tokens': 363, 'completion_tokens': 16, 'total_tokens': 379}}

# Ответ на промт "Нарисуй корову?"
# {'choices': [{'message': {'content': 'Запускаю генерацию изображения. Ожидайте результат <img src="a48a8516-acc7-41bc-9854-338c1434c553" fuse="true"/> - нарисовал для вас корову.', 'role': 'assistant', 'data_for_context': [{'content': 'Запускаю генерацию изображения. Ожидайте результат', 'role': 'assistant', 'function_call': {'name': 'text2image', 'arguments': {'query': 'cow, realistic, portrait'}}}, {'content': '{"status":"success"}', 'role': 'function', 'name': 'text2image'}, {'content': ' - нарисовал для вас корову.', 'role': 'assistant'}]}, 'index': 0, 'finish_reason': 'stop'}], 'created': 1716577823, 'model': 'GigaChat:3.1.25.3', 'object': 'chat.completion', 'usage': {'prompt_tokens': 364, 'completion_tokens': 41, 'total_tokens': 405}}

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# ШАГ2
# https://developers.sber.ru/docs/ru/gigachat/api/images-generation?lang=py
# Скачиваем изображение
# Для скачивания изображения передайте полученный идентификатор в запросе GET /files/{file_id}/content:

def get_chat_content(user_token, image_id, path):
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

# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# # ШАГ3
# # https://developers.sber.ru/docs/ru/gigachat/api/function-calling
# # Сохранение контекста
# # Для сохранения контекста после вызова встроенных функций, 
# # передавайте массив data_for_context в запросе в сообщениях с ролью assistant
# # {'content': 'Запускаю генерацию изображения. Ожидайте результат <img src="a48a8516-acc7-41bc-9854-338c1434c553" fuse="true"/> - нарисовал для вас корову.', 'role': 'assistant', 'data_for_context': [{'content': 'Запускаю генерацию изображения. Ожидайте результат', 'role': 'assistant', 'function_call': {'name': 'text2image', 'arguments': {'query': 'cow, realistic, portrait'}}}, {'content': '{"status":"success"}', 'role': 'function', 'name': 'text2image'}, {'content': ' - нарисовал для вас корову.', 'role': 'assistant'}]}

def get_chat_completions_updated(user_token, user_updated_message):

  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat",
    "messages": [
        
      # Предыдущий запрос
      # ЭТО УБРАТЬ! ПОХОЖЕ НЕ ТРЕБУЕТСЯ! ГЕНЕРИТ ЛУЧШЕ! ПРОВЕРЬ ЕЩЕ РАЗОК!
      # {
      #     "role": "user",
      #     "content": "Нарисуй кота, он играет в компьютерную игру, дом, вокруг еда, эффект тёплого света, мультяшный стиль."
      # },

      # Ответ на предыдущий запрос

      {'content': 'Запускаю генерацию изображения... <img src="72311e42-a508-47ca-ac42-f49f31c5edc8" fuse="true"/> - нарисовал город с небоскребом банка Сбербанк, город в космосе, вокруг планеты, эффект киберпанк, корпоративный стиль банка Сбербанк.', 'role': 'assistant', 'data_for_context': [{'content': 'Запускаю генерацию изображения...', 'role': 'assistant', 'function_call': {'name': 'text2image', 'arguments': {'query': 'Sberbank skyscraper, cyberpunk city, space, corporate style'}}}, {'content': '{"status":"success"}', 'role': 'function', 'name': 'text2image'}, {'content': ' - нарисовал город с небоскребом банка Сбербанк, город в космосе, вокруг планеты, эффект киберпанк, корпоративный стиль банка Сбербанк.', 'role': 'assistant'}]}, 
      
      #
      # {
      #     'content': 'Запускаю генерацию изображения... <img src="45f0e6b2-ec6b-4c39-ac40-b95214fad0fb" fuse="true"/> - нарисовал кота, который играет в компьютерную игру.', 
      #     'role': 'assistant', 
      #     'data_for_context': [
      #         {
      #             'content': 'Запускаю генерацию изображения...', 
      #             'role': 'assistant', 
      #             'function_call': {
      #                 'name': 'text2image', 
      #                 'arguments': {
      #                     'query': 'cat playing computer game, house, food, warm light, cartoon style, illustration'
      #                     }
      #                     }
      #                     }, 
      #                     {
      #                         'content': '{"status":"success"}', 
      #                         'role': 'function', 
      #                         'name': 'text2image'
      #                         }, 
      #                         {
      #                             'content': ' - нарисовал кота, который играет в компьютерную игру.', 
      #                             'role': 'assistant'
      #                             }
      #                             ]
      #                             },

      # Дополняем запрос
      
      {
          "role": "user",
          "content": user_updated_message
      }

    ],
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

  # content_text = response.json()["choices"][0]["message"]["content"]
  content = response.json()

  return content

user_updated_msg = "Дорисуй на небоскребе логотип сбербанка не меняя его, корпоративный стиль банка Сбербанк."
# content_response = get_chat_completions_updated(token, user_updated_msg)

# print(content_response)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Делаем диалоговую систему

def get_chat_completions_history(user_token, user_message, conversation_history=[]):
   
  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  # Если история диалога не предоставлена, инициализируем пустым списком
  if conversation_history is None:
    conversation_history = []

  conversation_history.append({
    "role": "user",
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


user_msg = "Лошадь пони в стиле цветочного сюрреализма на лугу,  вдохновленный природой камуфляж, цветочный панк, нежные материалы, яркая, студийная фотография. Стиль: Детальное фото."

response_img = get_chat_completions_history(token, user_msg)

# soup = BeautifulSoup(response_img[1]['content'], 'html.parser')

# img_src = soup.img['src']

# get_chat_content(token, img_src, "gen1")

print(response_img)

user_msg = "Дорисуй ей крылья ангела"

response_img = get_chat_completions_history(token, user_msg)

print(response_img)

# user_msg = "Нарисуй вместо яблок бананы"

# response_img = get_chat_completions_history(token, user_msg)

# print(response_img)

# get_chat_content(token, "01916c5e-a74d-44ae-9cb2-d1dd3b528caa", "gen1")
# get_chat_content(token, "080529e3-27e2-4579-ac9f-9e8a41aab333", "gen2")
# get_chat_content(token, "49da4e28-2607-425e-a8a2-e26c33c080c8", "gen3")


# Взаимодействие с Kandinsky через https://fusionbrain.ai/docs/ru/doc/api-dokumentaciya/
# YOUR_API_KEY = '5F87665812A0D4A0612C7BF845DC4B7E'
# YOUR_SECRET_KEY = '854CEA67B21CFBED1B6EA220EBB56983'

# import json
# import time

# import requests


# class Text2ImageAPI:

#     def __init__(self, url, api_key, secret_key):
#         self.URL = url
#         self.AUTH_HEADERS = {
#             'X-Key': f'Key {api_key}',
#             'X-Secret': f'Secret {secret_key}',
#         }

#     def get_model(self):
#         response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
#         data = response.json()
#         return data[0]['id']

#     def generate(self, prompt, model, images=1, width=1024, height=1024):
#         params = {
#             "type": "GENERATE",
#             "numImages": images,
#             "width": width,
#             "height": height,
#             "generateParams": {
#                 "query": f"{prompt}"
#             }
#         }

#         data = {
#             'model_id': (None, model),
#             'params': (None, json.dumps(params), 'application/json')
#         }
#         response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
#         data = response.json()
#         return data['uuid']

#     def check_generation(self, request_id, attempts=10, delay=10):
#         while attempts > 0:
#             response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
#             data = response.json()
#             if data['status'] == 'DONE':
#                 return data['images']

#             attempts -= 1
#             time.sleep(delay)


# if __name__ == '__main__':
#     api = Text2ImageAPI('https://api-key.fusionbrain.ai/', YOUR_API_KEY, YOUR_SECRET_KEY)
#     model_id = api.get_model()
#     uuid = api.generate("Sun in sky", model_id)
#     images = api.check_generation(uuid)
#     print(images)