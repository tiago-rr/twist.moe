#!/usr/bin/env python3

from os import getenv, path, mkdir, system
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
    episodes = input('Episodes to download ([start]/[end] or [episode] or "all"): ')
    if episodes == 'all':
        startEp = 1
        endEp = -1
    else:
        if '/' in episodes:
            try:
                startEp = int(episodes.split('/')[0])
                endEp = int(episodes.split('/')[1])
            except Exception as error:
                print('ERROR! Please use valid numbers!')
                exit()
            
            if startEp > endEp:
                print('\n')
                print('ERROR! End episode must be greater than the start episode!')
                exit()
        else:
            try:
                startEp = int(episodes)
                endEp = startEp
            except Exception as error:
                print('\n')
                print('ERROR! Please use valid numbers!')
                exit()

    useEnv = input("\nWould you like to use the .env's download path? [Y/n] ")
    if useEnv == 'y' or useEnv == 'Y':
        downloadPath = getenv('DOWNLOAD_PATH')
        print('Next time, you can use "-e" as a parameter to use the .env file.')
    else:
        downloadPath = input('\nInput the download path: ') + "/{}".format(slug)
        print('Download path: {}/{}'.format(downloadPath, slug))
elif len(argv) == 4:
    slug = argv[1]
    episodes = argv[2]
    downloadPath = argv[3]
    if downloadPath == '-e':
        downloadPath = getenv('DOWNLOAD_PATH')
    
    if episodes == 'all':
        startEp = 1
        endEp = -1
    else:
        if '/' in episodes:
            try:
                startEp = int(episodes.split('/')[0])
                endEp = int(episodes.split('/')[1])
            except Exception as error:
                print('ERROR! Please use valid numbers!')
                exit()
            
            if startEp > endEp:
                print('\n')
                print('ERROR! End episode must be greater than the start episode!')
                exit()
        else:
            try:
                startEp = int(episodes)
                endEp = startEp
            except Exception as error:
                print('\n')
                print('ERROR! Please use valid numbers!')
                exit()
    
else:
    print('\n')
    print('Too many or not enough arguments. Please use [slug] [[startEp/endEp]|[episode]|all] [[path/to/download]|-e], or use none and we will ask you.')
    exit()


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
    print('\n')
    print('There must be an anime file in the declared path!')
    exit()

if slug not in data:
    print('\n')
    print('The inputted anime slug must first be in the anime file. Use the start function to add it.')
    exit()

if not path.isdir(downloadPath):
    try:
        mkdir(downloadPath)
    except Exception as error:
        print('\n')
        print('Could not create the download path. Please do it manually.')
        exit()

downloadPath =  '{}/{}'.format(downloadPath, slug)

if endEp == -1 or endEp > len(data[slug]):
    endEp = len(data[slug])

if not path.isdir(downloadPath):
    mkdir(downloadPath)

print("\nDownloading {}'s {} episode(s)...".format(slug, endEp - startEp + 1))
if startEp < endEp:
    for index in range(startEp - 1, endEp - 1):
        link = data[slug][index]
        print('Downloading episode {}...'.format(index + 1))
        system('bash down.sh {} {}-{}.mp4 {}'.format(downloadPath, slug, "{:03d}".format(index + 1), link))
else:
    link = data[slug][startEp - 1]
    print('Downloading episode {}...'.format(startEp))
    system('bash down.sh {} {}-{}.mp4 {}'.format(downloadPath, slug, "{:03d}".format(startEp), link))