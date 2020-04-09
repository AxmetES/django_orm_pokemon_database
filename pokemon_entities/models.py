from django.db import models


class Pokemon(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title_ru = models.CharField(max_length=200, default=True)
    title_en = models.CharField(max_length=200, default=True)
    title_jp = models.CharField(max_length=200, default=True)
    image = models.URLField()
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField(default=True)
    health = models.IntegerField(default=True)
    attack = models.IntegerField(default=True)
    defence = models.IntegerField(default=True)
    stamina = models.IntegerField(default=True)
    description = models.TextField(blank=True, null=True)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Pokemon {self.title_ru}, {self.title_en}, {self.title_jp}'


class PokemonEntity(models.Model):
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
