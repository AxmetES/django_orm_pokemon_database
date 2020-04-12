import datetime

from django.db import models


class Pokemon(models.Model):
    """Покемон"""
    title_ru = models.CharField(max_length=200, default='Default title', blank=True, verbose_name='название рус.')
    title_en = models.CharField(max_length=200, default='Default title', blank=True, verbose_name='название анл.')
    title_jp = models.CharField(max_length=200, default='Default title', blank=True, verbose_name='название япн.')
    image = models.URLField(verbose_name='изображение', blank=True)
    description = models.TextField(blank=True, verbose_name='описание')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='parents',
                               verbose_name='эволюция')

    def __str__(self):
        return f'Pokemon {self.title_ru}'


class PokemonEntity(models.Model):
    """Особь"""
    lat = models.FloatField(verbose_name='широта')
    lon = models.FloatField(verbose_name='долгота')

    appeared_at = models.DateTimeField(null=True, blank=True, verbose_name='появился в')
    disappeared_at = models.DateTimeField(null=True, blank=True, verbose_name='исчез в')

    level = models.IntegerField(null=True, verbose_name='уровень')
    health = models.IntegerField(null=True, verbose_name='здоровье')
    attack = models.IntegerField(null=True, verbose_name='атака')
    defence = models.IntegerField(null=True, verbose_name='защита')
    stamina = models.IntegerField(null=True, verbose_name='выносливость')

    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='связи')
