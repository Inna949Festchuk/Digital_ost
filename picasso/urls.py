from django.urls import path

from picasso.views import (
    AudioView,
    TextView,
    ClearView,
    record_audio, 
    )

urlpatterns = [
    path('record-audio/', record_audio), # Стартовая страница, запуск микрафона
    path('api/audio/', AudioView.as_view(), name='createaudiofile'), 
    path('api/text/', TextView.as_view(), name='createtextfile'),
    path('api/clear/', ClearView.as_view(), name='clearfile'), 

    
]

