from django.db import models


class Pokemon(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pokemons', null=True)
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField(default=True)
    health = models.IntegerField(default=True)
    attack = models.IntegerField(default=True)
    defence = models.IntegerField(default=True)
    stamina = models.IntegerField(default=True)
    # entity = models.ForeignKey(on_delete=)

    def __str__(self):
        return f'Pokemon {self.title}'


class PokemonEntity(models.Model):
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

