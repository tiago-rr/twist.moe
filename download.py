#!/usr/bin/env python3

from os import getenv, path, mkdir
from dotenv import load_dotenv
from json import load, dump
from urllib import request
from sys import argv
import requests
load_dotenv()

slug = None
startEp = 0
endEp = 0
downloadPath = None

if len(argv) == 1:
    print('Download configuration: ')
    slug = input("\nAnime slug: ")
    episodes = input('Episodes to download ([start]/[end] or "all"): ')
    if episodes == 'all':
        startEp = 1
        endEp = -1
    else:
        if '/' in episodes:
            #TODO: convert to try/except to catch errors
            startEp = int(episodes.split('/')[0])
            endEp = int(episodes.split('/')[1])
            #TODO: check if start < end
        else:
            #TODO: must be start-end
            exit()
    useEnv = input("\nWould you like to use the .env's download path? [Y/n] ")
    if useEnv == 'y' or useEnv == 'Y':
        downloadPath = getenv('DOWNLOAD_PATH')
        print('Next time, you can use "-e" as a parameter to use the .env file.')
    else:
        downloadPath = input('\nInput the download path: ') + "/{}".format(slug)

        print('Download path: {}/{}'.format(downloadPath, slug))
animePath = getenv("ANIME_JSON_PATH")
header = {
    'x-access-token': getenv('HEADER_AUTH')
}
apiUrl = getenv("API_URL")
twistUrl = getenv('TWIST_URL')

data = {}
if path.isfile(animePath):
    with open(animePath, 'r') as infile:
        data = load(infile)
else:
    #TODO: animeFile doesn't exist
    exit()

if slug not in data:
    #TODO: invalid slug, please add it first
    exit()

if not path.isdir(downloadPath):
    mkdir(downloadPath)

downloadPath =  '{}/{}'.format(downloadPath, slug)

if endEp == -1 or endEp > len(data[slug]):
    endEp = len(data[slug])

if not path.isdir(downloadPath):
    mkdir(downloadPath)

print("\nDownloading {}'s {} episode(s)...".format(slug, endEp - startEp + 1))
for index in range(startEp - 1, endEp - 1):
    link = data[slug][index]
    print('Episode {}:'.format(index + 1))
    #TODO: download