# Generated by Django 4.0.1 on 2022-02-06 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='type',
            new_name='mtype',
        ),
        migrations.AlterField(
            model_name='message',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.room', verbose_name='rooms'),
        ),
        migrations.AlterField(
            model_name='room',
            name='rid',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
    ]
