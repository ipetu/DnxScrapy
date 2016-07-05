#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Liuwf on 16/6/28
from __future__ import unicode_literals

from youtube_dl import YoutubeDL

import errno
import io
import json
import os.path
import re
import types


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


downloadPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/dowload/"
ydl_opts = {
    "outtmpl": downloadPath + "%(id)s.%(ext)s",
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4'
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}


def get_params(override=None):
    PARAMETERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "parameters.json")
    LOCAL_PARAMETERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "local_parameters.json")
    with io.open(PARAMETERS_FILE, encoding='utf-8') as pf:
        parameters = json.load(pf)
    if os.path.exists(LOCAL_PARAMETERS_FILE):
        with io.open(LOCAL_PARAMETERS_FILE, encoding='utf-8') as pf:
            parameters.update(json.load(pf))
    if override:
        parameters.update(override)
    return parameters


def try_rm(filename):
    """ Remove a file if it exists """
    try:
        os.remove(filename)
    except OSError as ose:
        if ose.errno != errno.ENOENT:
            raise


class DnxFakeYDL(YoutubeDL):
    def __init__(self, override=None):
        # Different instances of the downloader can't share the same dictionary
        # some test set the "sublang" parameter, which would break the md5 checks.
        params = get_params(override=override)
        super(DnxFakeYDL, self).__init__(params, auto_init=True)
        self.result = []

    def to_screen(self, s, skip_eol=None):
        print(s)

    def trouble(self, s, tb=None):
        raise Exception(s)

    # def download(self, x):
    #     self.result.append(x)

    def expect_warning(self, regex):
        # Silence an expected warning matching a regex
        old_report_warning = self.report_warning

        def report_warning(self, message):
            if re.match(regex, message):
                return
            old_report_warning(message)

        self.report_warning = types.MethodType(report_warning, self)


class ytbDownload(DnxFakeYDL):
    def __init__(self, *args, **kwargs):
        super(ytbDownload, self, ).__init__(ydl_opts, *args, **kwargs)
        # self.downloaded_info_dicts = []
        self.msgs = []

    def startDownload(self):
        playList = ['https://www.youtube.com/watch?v=cmnX7iYK1Nk', 'https://www.youtube.com/watch?v=6Lwkkem7hMw',
                    'https://www.youtube.com/watch?v=b_qsx9uNhi0']
        # self.add_extra_info(info_dict=info_dict, extra_info=None)
        # result = self.extract_info(url="https://www.youtube.com/watch?v=cmnX7iYK1Nk", download=True)
        # print result
        self.download(playList)


if __name__ == '__main__':
    ytb = ytbDownload()
    ytb.startDownload()
