# Generated by Django 3.2.8 on 2021-10-28 04:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mega_files', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='megafile',
            name='binary',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mega_files.megabinary'),
        ),
        migrations.AlterField(
            model_name='megafile',
            name='id',
            field=models.CharField(default=uuid.UUID('6e65730e-689d-44c2-b779-e15b1cd74eea'), max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='megafile',
            name='serverFileName',
            field=models.CharField(default=281213617849348668436740071521610345770, max_length=239),
        ),
    ]
