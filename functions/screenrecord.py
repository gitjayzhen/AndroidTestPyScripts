#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import string
import sys
import time

from utils import androiddebug

# 需要Android4.4及4.4以上版本，运行脚本后可录制设备上的操作，默认使用手机分辨率，时间3min。手动按Enter结束录制。
# 录制结果存放于当前目录下的video目录下

PATH = lambda p: os.path.abspath(p)

def record():
    androiddebug.shell("screenrecord /data/local/tmp/video.mp4")
    input_key = raw_input("Please press the Enter key to stop recording:\n")
    if input_key == "":
        androiddebug.adb("kill-server")

    print "Get Video file..."
    androiddebug.adb("start-server")
    time.sleep(1.5)

    path = PATH("%s/video" %os.getcwd())
    if not os.path.isdir(path):
        os.makedirs(path)

    androiddebug.adb("pull /data/local/tmp/video.mp4 %s" % PATH("%s/%s.mp4" % (path, androiddebug.timestamp()))).wait()

if __name__ == "__main__":
    sdk = string.atoi(androiddebug.shell("getprop ro.build.version.sdk").stdout.read())
    if sdk < 19:
        print ">>> sdk version is %s, less than 19!"
        sys.exit(0)
    else:
        record()
        print "Completed"
