# Generated by Django 5.0 on 2024-05-04 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcription', '0002_recording_delete_audiofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_file', models.FileField(upload_to='audio/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Commands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commands', models.CharField(help_text='Введите команды', max_length=250, verbose_name='Название команды')),
                ('confirmation', models.CharField(help_text='Текст подтверждения команды', max_length=250, verbose_name='Текст подтверждения')),
                ('slug', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='UsersTexts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usertext', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.DeleteModel(
            name='Recording',
        ),
        migrations.AddIndex(
            model_name='commands',
            index=models.Index(fields=['commands'], name='transcripti_command_abf8b0_idx'),
        ),
    ]
