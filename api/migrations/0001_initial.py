# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-11 11:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_1_bet', models.IntegerField()),
                ('team_2_bet', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(default='', max_length=20)),
                ('start_date', models.DateTimeField()),
                ('stop_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goals', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=100)),
                ('description', models.TextField(default='')),
                ('color', models.CharField(default='', max_length=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_1_goals', models.IntegerField()),
                ('team_2_goals', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='api.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start_date', models.DateTimeField()),
                ('stop_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SpecialBet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_goals', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Player')),
            ],
        ),
        migrations.CreateModel(
            name='SpecialBetFinal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goals', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('players', models.ManyToManyField(to='api.Player')),
            ],
        ),
        migrations.CreateModel(
            name='SpecialBetResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.IntegerField()),
                ('goals', models.IntegerField()),
                ('team', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('country', models.CharField(default='', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('color', models.CharField(default='', max_length=7)),
                ('start_date', models.DateTimeField()),
                ('stop_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='specialbetresult',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Tournament'),
        ),
        migrations.AddField(
            model_name='specialbetresult',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='special_bet_results', to='api.User'),
        ),
        migrations.AddField(
            model_name='specialbetfinal',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Team'),
        ),
        migrations.AddField(
            model_name='specialbetfinal',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Tournament'),
        ),
        migrations.AddField(
            model_name='specialbet',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Team'),
        ),
        migrations.AddField(
            model_name='specialbet',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Tournament'),
        ),
        migrations.AddField(
            model_name='specialbet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='special_bets', to='api.User'),
        ),
        migrations.AddField(
            model_name='round',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Tournament'),
        ),
        migrations.AddField(
            model_name='point',
            name='result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Result'),
        ),
        migrations.AddField(
            model_name='point',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points', to='api.User'),
        ),
        migrations.AddField(
            model_name='player',
            name='teams',
            field=models.ManyToManyField(to='api.Team'),
        ),
        migrations.AddField(
            model_name='group',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to='api.User'),
        ),
        migrations.AddField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(related_name='groups', to='api.User'),
        ),
        migrations.AddField(
            model_name='goal',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='round',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='api.Round'),
        ),
        migrations.AddField(
            model_name='game',
            name='team_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_1', to='api.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='team_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_2', to='api.Team'),
        ),
        migrations.AddField(
            model_name='bet',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Game'),
        ),
        migrations.AddField(
            model_name='bet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bets', to='api.User'),
        ),
        migrations.AlterUniqueTogether(
            name='specialbetresult',
            unique_together=set([('user', 'tournament')]),
        ),
        migrations.AlterUniqueTogether(
            name='point',
            unique_together=set([('user', 'result')]),
        ),
    ]
