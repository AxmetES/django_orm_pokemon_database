import folium

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
        pokemon_entity = PokemonEntity.objects.filter(pokemon__id=pokemon.id)
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
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)

    except:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    kids = pokemon.parents.all()
    requested_pokemon = PokemonEntity.objects.filter(pokemon__id=pokemon.id)
    pokemons_on_page = {
        "pokemon_id": pokemon.id,
        "title_ru": pokemon.title_ru,
        "title_en": pokemon.title_en,
        "title_jp": pokemon.title_jp,
        "description": pokemon.description,
        "img_url": pokemon.image,
        'previous_evolution': {},
        'next_evolution': {}
    }
    if pokemon.parent is not None:
        print('parent')
        pokemons_on_page['previous_evolution'] = {
            "title_ru": pokemon.parent.title_ru,
            "pokemon_id": pokemon.parent.id,
            "img_url": pokemon.parent.image,
        }
    if kids.exists():
        pokemons_on_page['next_evolution'] = {
            "title_ru": kids[0].title_ru,
            "pokemon_id": kids[0].id,
            "img_url": kids[0].image,
        }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon.title_ru, pokemon.image)

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemons_on_page})
