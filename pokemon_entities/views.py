import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        id = pokemon.id
        pokemon_entity = PokemonEntity.objects.filter(pokemon__id__contains=id)
        for entity in pokemon_entity:
            add_pokemon(
                folium_map, entity.lat, entity.lon,
                pokemon.title_ru, pokemon.image)

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image,
            'title_ru': pokemon.title_ru,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemons = Pokemon.objects.all()

    for pokemon in pokemons:
        if pokemon.id == int(pokemon_id):
            print(pokemon.title_ru)
            requested_pokemon = PokemonEntity.objects.filter(pokemon__id=pokemon_id)
            parent = Pokemon.objects.get(pokemon__id=pokemon.parent_id)
            pokemons_info = {
                "pokemon_id": pokemon.id,
                "title_ru": pokemon.title_ru,
                "title_en": pokemon.title_en,
                "title_jp": pokemon.title_jp,
                "description": pokemon.description,
                "img_url": pokemon.image,
                'parent':pokemon.parent_id,
                "previous_evolution": {
                    "title_ru": parent.title_ru,
                    "pokemon_id": parent.id,
                    "img_url": parent.image,
                }
            }
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon.title_ru, pokemon.image)

    print(pokemons_info["pokemon_id"])
    print(pokemons_info["title_ru"])
    print(pokemons_info["title_en"])
    print(pokemons_info["title_jp"])
    print(pokemons_info["parent"])

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemons_info})
