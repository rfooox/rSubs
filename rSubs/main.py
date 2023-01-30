# -*- coding: utf-8 -*-
import argparse
import os
import logging
from rSubs.subtitle_downloader import SubtitleDownloader


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version=SubtitleDownloader.version(),
                        help=u'show version info'
                        )
    parser.add_argument('-c', '--cid', action='store_true', help=u'show file cid info')
    # parser.add_argument('-d', '--download', action='store', help=u'download subtitles with cid')
    parser.add_argument('-l', '--loop', action='store_true', dest='loop', default=False,
                        help=u'watch a directory recursively, automatically download '
                             u'subtitles when an aria2 task finishes'
                        )
    parser.add_argument('dest', action='store', default='.',
                        help=u'path of directory or video file you need to download subtitles for')

    params = parser.parse_args()
    # 获取文件cid
    if params.cid:
        if os.path.isfile(params.dest):
            temp_cid = SubtitleDownloader.cid_hash_file(params.dest)
            logging.info(f"{params.dest} cid: {temp_cid}")

    # 判断是否为监测文件夹变动
    if params.loop:
        if os.path.isdir(params.dest):
            logging.info(u"Running...")
            # 监测文件夹 执行loop
            SubtitleDownloader.inotify_loop(params.dest)
        else:
            # 不是文件夹 退出监测
            logging.error(u"The given path is invalid.")
    else:
        # 执行 下载任务（参数为文件夹或者文件）
        SubtitleDownloader.download_subtitle(params.dest)
    logging.info(u"Bye :)")


if __name__ == '__main__':
    main()
