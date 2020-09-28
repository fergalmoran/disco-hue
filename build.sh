#!/usr/bin/env sh
docker run \
    -v "$(pwd):/src/" \
    fergalmoran/disco-hue-builder:linux