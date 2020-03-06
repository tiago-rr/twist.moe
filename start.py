#!/usr/bin/env python3

from dotenv import load_dotenv
from json import load, dump
from os import getenv, path
from sys import argv
import requests
import decrypt
load_dotenv()

def getDownloadLinks(fullApiUrl):
    links = []
    response = requests.get('{}/sources'.format(fullApiUrl), headers=header)
    for source in response.json():
        decrypted = decrypt.decrypt_single(source['source'])
        episodeLink = '{}{}'.format(twistUrl, decrypted)
        links.append(episodeLink)
    return links

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
    print('That anime is already in your JSON file. It will now be updated.')

    links = getDownloadLinks(fullApiUrl)
    if len(links) > len(data[slug]):
        diff = len(links) - len(data[slug])
        data[slug] = links
        with open(animePath, 'w') as outfile:
            dump(data, outfile, indent=4)

        print('Anime "{}" has been update with {} new episodes!'.format(slug, diff))
    else:
        print('"{}" is already up-to-date with {} episodes.'.format(slug, len(links)))
else:
    data[slug] = getDownloadLinks(fullApiUrl)
    
    with open(animePath, 'w') as outfile:
        dump(data, outfile, indent=4)

    print('Anime "{}" has been added to your JSON file with {} episodes!'.format(slug, len(data[slug])))