#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Liuwf on 16/6/28
from __future__ import unicode_literals
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        print 'msgDebug-->' + msg

    def warning(self, msg):
        print 'msgWarning-->' + msg

    def error(self, msg):
        print 'msgError--->' + msg


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'mp4',
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4'
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'outtmpl': '%(id)s.%(ext)s',
    'writeinfojson': True,
    'ignoreerrors': True,
    'simulate': True,
}

ydl = youtube_dl.YoutubeDL(ydl_opts)
playList = ['https://www.youtube.com/watch?v=cmnX7iYK1Nk', 'https://www.youtube.com/watch?v=6Lwkkem7hMw',
            'https://www.youtube.com/watch?v=b_qsx9uNhi0']
with ydl:
    # result = ydl.extract_info(
    #     ['https://www.youtube.com/watch?v=cmnX7iYK1Nk', 'https://www.youtube.com/watch?v=6Lwkkem7hMw',
    #      'https://www.youtube.com/watch?v=b_qsx9uNhi0'],
    #     download=False  # We just want to extract the info
    # )
    # result = ydl.download(playList)
    ydl.list_formats()
# if 'entries' in result:
#     # Can be a playlist or a list of videos
#     video = result['entries'][0]
# else:
#     # Just a video
#     video = result
#
# print(video)
# video_url = video['url']
# print(video_url)
