from rest_framework import serializers

from transcription.models import UsersTexts

class AudioFileSerializer(serializers.Serializer):
    '''FileField используется для загрузки и обработки 
    файлов, в данном случае - для работы с аудио файлами. 
    При использовании этого сериализатора, клиент может 
    отправлять файлы аудио на сервер для последующей 
    обработки.
    '''
    audio = serializers.FileField()

class UsersTextsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersTexts
        fields = ['usertext', 'created', ] 

