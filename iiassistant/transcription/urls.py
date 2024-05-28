from django.urls import path

from transcription.views import (
    CreateAudioView, 
    CheckBalanceAPIView,
    SendMoneyAPIView,
    record_audio, 
    # sound_in_text,
    # search, 
    # trgm_search,
    )

urlpatterns = [
    path('record-audio/', record_audio), # Стартовая страница, запуск микрафона
    path('api/create-audio/', CreateAudioView.as_view(), name='createaudio'), # Обработка audioBlob с микравона 
                                                                            # (rest api - подключена к кнопке StopRecording)
    # path('create_text/', sound_in_text), # Запуск нейронки vosk
    # path('search/', search), # Полнотекстовый поиск
    # path('trgm-search/', trgm_search), # Триграммный поиск

    path('api/proverit/', CheckBalanceAPIView.as_view(), name='execute_check_balance'),
    path('api/otpravit/', SendMoneyAPIView.as_view(), name='execute_send_money'),
    # path('api/novaya/', NewAPIView.as_view(), name='execute_send_money'),
]

