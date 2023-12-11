# Generated by Django 4.2.8 on 2023-12-08 21:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=155)),
                ('profile_image', models.ImageField(max_length=155, upload_to=None)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series_name', models.CharField(max_length=155)),
                ('episode_name', models.CharField(max_length=155)),
                ('serial', models.SlugField(default='')),
                ('description', models.TextField()),
                ('image', models.ImageField(max_length=155, upload_to=None)),
                ('rating', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=155)),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlist_creator', to='playlistapi.creator')),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episode', to='playlistapi.episode')),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=155)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator_id', to='playlistapi.creator')),
            ],
        ),
        migrations.CreateModel(
            name='EpisodeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episode_tag', to='playlistapi.episode')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag', to='playlistapi.tag')),
            ],
        ),
        migrations.AddField(
            model_name='episode',
            name='tags',
            field=models.ManyToManyField(through='playlistapi.EpisodeTag', to='playlistapi.tag'),
        ),
    ]