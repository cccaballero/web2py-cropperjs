#! /usr/bin/env sh

rm web2py.plugin.cropperjs.w2p
tar czvf web2py.plugin.cropperjs.w2p --exclude='*.sh'  --exclude='*.md' --exclude='LICENSE' --exclude='*.pyc' --exclude='__pycache__' *
