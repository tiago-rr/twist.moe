#!/bin/bash
cd $1
curl -L -o $2 -C - "$3" -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36' -H "Referer: https://twist.moe/"
cd