#!/bin/bash
v4l2-ctl -d /dev/video1 --list-ctrls
v4l2-ctl -d /dev/video1 --set-ctrl focus_auto=0
v4l2-ctl -d /dev/video1 --set-ctrl focus_absolute=255
echo "Changes successful"
v4l2-ctl -d /dev/video1 --list-ctrls