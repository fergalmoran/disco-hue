#!/usr/bin/env sh
docker run -v "$(pwd):/src/" \
    --entrypoint /bin/sh \
    cdrx/pyinstaller-linux \
    -c "apt-get update -y && apt-get install -y portaudio19-dev && /entrypoint.sh"
