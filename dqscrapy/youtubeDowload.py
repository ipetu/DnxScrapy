#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Liuwf on 16/6/28
import youtube_dl

ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

with ydl:
    result = ydl.extract_info(
        'http://v.youku.com/v_show/id_XMTYyMTk4OTU0OA==.html?f=26378220&from=y1.3-idx-beta-1519-23042.223465.4-3',
        download=False # We just want to extract the info
    )

if 'entries' in result:
    # Can be a playlist or a list of videos
    video = result['entries'][0]
else:
    # Just a video
    video = result

print(video)
video_url = video['url']
print(video_url)
