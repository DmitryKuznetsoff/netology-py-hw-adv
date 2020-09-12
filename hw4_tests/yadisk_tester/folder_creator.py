import requests
import os


def create_folder(folder_name):
    url = 'https://cloud-api.yandex.net:443/v1/disk/resources'
    headers = {'Authorization': 'OAuth ' + os.getenv('YANDEX_DISK_API_KEY')}
    params = {'path': folder_name}

    r = requests.put(url, headers=headers, params=params)
    return r.status_code
