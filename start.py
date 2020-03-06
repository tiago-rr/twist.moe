#!/usr/bin/env python3

from dotenv import load_dotenv
from json import load, dump
from os import getenv, path
from sys import argv
import requests
import decrypt
load_dotenv()

animePath = getenv("ANIME_JSON_PATH")
header = {
    'x-access-token': getenv('HEADER_AUTH')
}
apiUrl = getenv("API_URL")
twistUrl = getenv('TWIST_URL')
slug = argv[1]

data = {}
if path.isfile(animePath):
    with open(animePath, 'r') as infile:
        data = load(infile)

fullApiUrl = '{}/{}'.format(apiUrl, slug)

slugValid = requests.get(fullApiUrl, headers=header).status_code == 200
if not slugValid:
    # TODO: slug invalid/unknown
    exit()

if slug in data:
    # TODO: slug already in data
    exit()

response = requests.get('{}/sources'.format(fullApiUrl), headers=header)
for source in response.json():
    decrypted = decrypt.decrypt_single(source['source'])
    episodeLink = '{}{}'.format(twistUrl, decrypted)
    print(episodeLink)
    # TODO: decrypt each source
    exit()