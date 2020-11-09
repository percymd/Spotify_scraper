import base64
import requests
import pandas as pd


def get_token(client_id, client_secret):

    client_str = '{client_id}:{client_secret}'.format(client_id=client_id, client_secret=client_secret)
    client_encode = base64.b64encode(client_str.encode("utf-8"))  # Codificado en Bytes
    client_encode = str(client_encode, "utf-8")  # Codificado en String

    token_url = 'https://accounts.spotify.com/api/token'
    params = {'grant_type': 'client_credentials'}
    headers= {'Authorization' : 'Basic {client_encode}'.format(client_encode=client_encode)}

    r = requests.post(token_url, data=params, headers = headers)

    if r.status_code != 200:
        print('Error en la request.', r.json())
        return None
    print('Token valido por {} segundos.'.format(r.json()['expires_in']))
    return r.json()['access_token']


def obtener_discografia(artist_id, token, return_name = False, page_limit = 50, country = None):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
    header = {'authorization': f'Bearer {token}'}
    params = {'limit': page_limit,
              'offset': 0,
              'country': country}

    lista = []
    r = requests.get(url, params = params, headers = header)

    if r.status_code != 200:
        print('Error en la request', r.json())
        return None

    if return_name:
        lista += [(item['id'], item['name']) for item in r.json()['items']]
    else:
        lista += [item['id'] for item in r.json()['items']]

    while r.json()['next']:
        r = requests.get(r.json()['next'], headers = header)

        if r.status_code != 200:
            print('Error en la request', r.json())
        else:
            if return_name:
                lista += [(item['id'], item['name']) for item in r.json()['items']]
            else:
                lista += [item['id'] for item in r.json()['items']]

    return lista
    

def obtener_tracks(album_id, token, return_name = False, page_limit = 50, country = None):
    url = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
    header = {'authorization': f'Bearer {token}'}
    params = {'limit': page_limit,
              'offset': 0,
              'country': country}

    lista = []
    r = requests.get(url, params = params, headers = header)

    if r.status_code != 200:
        print('Error en la request', r.json())
        return None

    if return_name:
        lista += [(item['id'], item['name']) for item in r.json()['items']]
    else:
        lista += [item['id'] for item in r.json()['items']]

    while r.json()['next']:
        r = requests.get(r.json()['next'], headers = header)

        if r.status_code != 200:
            print('Error en la request', r.json())
        else:
            if return_name:
                lista += [(item['id'], item['name']) for item in r.json()['items']]
            else:
                lista += [item['id'] for item in r.json()['items']]

    return lista

def main():
 
    id_blink = '6FBDaR13swtiWwGhX1WQsP'
    client_id = 'your_id'
    client_secret = 'your_secret_id'

    token = get_token(client_id, client_secret)

    print(token)

    lista_albums = obtener_discografia(id_blink, token, True, country = 'PE')

    discography = {}
    for album in lista_albums:
        lista_tracks = obtener_tracks(album[0], token, True, country = 'PE')
        tracks_name = [tracks[1] for tracks in lista_tracks]
        discography[f'{album[1]}'] = tracks_name

    df = pd.DataFrame({key:pd.Series(value) for key, value in discography.items()})
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', 30)

    df.to_excel('Discography.xlsx', sheet_name='Hoja_1')

if __name__ == "__main__":
    main()