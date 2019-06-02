from pathlib import PurePosixPath
from urllib.parse import urlparse

import requests
from flask import Flask, request, Response

app = Flask(__name__)

FFMPEG_PATH = '/usr/bin/ffmpeg'
PIPE_URL = 'pipe://{ffmpeg_path} -i "{stream_url}" -c copy -f mpegts pipe:1'


def is_url_hls(url: str):
    if url.startswith('http'):
        return PurePosixPath(urlparse(url).path).name.endswith('.m3u8')


@app.route('/')
def m3upipe():
    url = request.args.get('url', type=str)

    playlist = requests.get(url)

    output = []

    for line in playlist.text.split('\n'):
        line = line.strip()
        if is_url_hls(line):
            line = PIPE_URL.format(ffmpeg_path=FFMPEG_PATH, stream_url=line)

        output.append(line)

    filename = 'playlist.m3u'

    resp = Response('\n'.join(output), mimetype='audio/x-mpegurl')
    resp.headers['Content-Disposition'] = f'attachment; filename={filename}'

    return resp


if __name__ == '__main__':
    app.run()
