from django.urls import path

from picasso.views import (
    AudioView,
    record_audio, 
    )

urlpatterns = [
    path('record-audio/', record_audio), # Стартовая страница, запуск микрафона
    path('api/audio/', AudioView.as_view(), name='createaudiofile'), # Обработка audioBlob с микравона 
                                                                            # (rest api - подключена к кнопке StopRecording)
    
]
