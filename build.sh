#!/bin/bash
set -e

uv run pyinstaller --noconfirm --onedir --windowed --name=CTkKnapsack src/ctkknapsack/__main__.py

wget -v https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
chmod +x linuxdeploy-x86_64.AppImage

mkdir -p AppDir/usr/bin
cp -r dist/CTkKnapsack/* AppDir/usr/bin/

touch ctkknapsack.svg

./linuxdeploy-x86_64.AppImage --appdir=AppDir -d ctkknapsack.desktop -i ctkknapsack.svg --output appimage
