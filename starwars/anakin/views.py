from django.shortcuts import render
import requests
try:
    import certifi
    CA_BUNDLE = certifi.where()
except Exception:
    # If certifi is not available, keep default verification (True)
    CA_BUNDLE = True

# Create your views here.

def anakin_view(request):
    return render(request, 'home.html')


def starwars_api(request):
    try:
        resp = requests.get('https://swapi.info/api/people/1/', timeout=5, verify=CA_BUNDLE)
        if resp.status_code == 200:
            data = resp.json()
        else:
            data = {'error': f'API response {resp.status_code}'}
    except Exception as e:
        # Si `requests` no está instalado o hay fallo de red, capturamos el error
        data = {'error': str(e)}

    return render(request, 'starwars_api.html', {'data': data})





def people_list(request):
    """Muestra listado paginado de personajes desde SWAPI con búsqueda."""
    page = request.GET.get('page', '1')
    q = request.GET.get('q', '').strip()
    params = {'page': page}
    if q:
        params['search'] = q

    try:
        resp = requests.get('https://swapi.info/api/people/', params=params, timeout=5, verify=CA_BUNDLE)
        resp.raise_for_status()
        payload = resp.json()
    except Exception as e:
        payload = {'results': [], 'count': 0, 'next': None, 'previous': None, 'error': str(e)}

    # If the API returned a bare list (instead of a dict with 'results'), normalize it
    if isinstance(payload, list):
        payload = {
            'results': payload,
            'count': len(payload),
            'next': None,
            'previous': None,
        }

    # Extract id from resource URL for each result
    results = []
    for item in payload.get('results', []):
        url = item.get('url', '')
        # url like https://swapi.dev/api/people/1/
        pk = None
        try:
            pk = int(url.rstrip('/').split('/')[-1])
        except Exception:
            pk = None
        # Image source from starwars-visualguide (works for many SW characters)
        image = None
        if pk:
            image = f'https://starwars-visualguide.com/assets/img/characters/{pk}.jpg'

        results.append({
            'pk': pk,
            'name': item.get('name'),
            'gender': item.get('gender'),
            'birth_year': item.get('birth_year'),
            'image': image,
        })

    context = {
        'results': results,
        'count': payload.get('count', 0),
        'next': payload.get('next'),
        'previous': payload.get('previous'),
        'error': payload.get('error'),
        'q': q,
        'page': int(page) if str(page).isdigit() else 1,
    }

    return render(request, 'people_list.html', context)


def people_detail(request, pk):
    """Muestra detalle de un personaje por id (pk) consultando SWAPI."""
    try:
        resp = requests.get(f'https://swapi.info/api/people/{pk}/', timeout=5, verify=CA_BUNDLE)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        data = {'error': str(e)}

    # Map to required fields: nombre, sexo, edad (usamos birth_year de la API)
    image = f'https://starwars-visualguide.com/assets/img/characters/{pk}.jpg' if pk else None

    detail = {
        'name': data.get('name'),
        'gender': data.get('gender'),
        'birth_year': data.get('birth_year'),
        'image': image,
        'error': data.get('error') if 'error' in data else None,
    }

    return render(request, 'people_detail.html', {'detail': detail})



def films_api(request):
    url = f"https://swapi.info/api/films/"
    try:
        resp = requests.get(url, timeout=5, verify=CA_BUNDLE)
        resp.raise_for_status()
        data = resp.json()
        print(data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching films: {e}")
        data = {'results': []}
        return render(requests.request, 'films_api.html', {'films': data.get('results', [])})

    # If API returned a bare list, adapt it to expected structure
    if isinstance(data, list):
        films = data
    else:
        films = data.get('results', [])

    return render(request, 'films_api.html', {'films': films})


def films_list(request):
    page = request.GET.get('page', '1')
    q = request.GET.get('q', '').strip()
    params = {'page': page}
    if q:
        params['search'] = q

    try:
        resp = requests.get('https://swapi.info/api/films/', params=params, timeout=5, verify=CA_BUNDLE)
        resp.raise_for_status()
        payload = resp.json()
    except Exception as e:
        payload = {'results': [], 'count': 0, 'next': None, 'previous': None, 'error': str(e)}

    # If the API returned a bare list (instead of a dict with 'results'), normalize it
    if isinstance(payload, list):
        payload = {
            'results': payload,
            'count': len(payload),
            'next': None,
            'previous': None,
        }

    results = payload.get('results', [])

    context = {
        'results': results,
        'count': payload.get('count', 0),
        'next': payload.get('next'),
        'previous': payload.get('previous'),
        'error': payload.get('error'),
        'q': q,
        'page': int(page) if str(page).isdigit() else 1,
    }

    return render(request, 'films_list.html', context)



def films_detail(request, pk):
    """Muestra detalle de una pelicula por id (pk) consultando SWAPI."""
    try:
        resp = requests.get(f'https://swapi.info/api/films/{pk}/', timeout=5, verify=CA_BUNDLE)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        data = {'error': str(e)}

    detail = {
        'title': data.get('title'),
        'director': data.get('director'),
        'producer': data.get('producer'),
        'release_date': data.get('release_date'),
        'opening_crawl': data.get('opening_crawl'),
        'error': data.get('error') if 'error' in data else None,
    }

    return render(request, 'films_detail.html', {'detail': detail})