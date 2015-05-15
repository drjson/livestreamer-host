#!/usr/bin/env python

from __future__ import print_function

from flask import Flask, Response, abort
from livestreamer import Livestreamer, StreamError, PluginError, NoPluginError

app = Flask(__name__)


@app.route('/w/<path:url>/<quality>')
def watch(url, quality):
    """Open a stream based on URL/quality and send it back"""

    stream = openStream(url, quality)

    try:
        sd = stream.open()
    except StreamError:
        abort(404)

    return Response(playStream(sd),
                    mimetype="video/unknown")


# Generator to play data
def playStream(sd, chunkSize=8192):
    """Generator to return data in the stream reader"""
    try:
        while True:
            try:
                data = sd.read(chunkSize)
            except IOError as err:
                print("Failed to read data from stream: {0}".format(err))
                raise StopIteration

            if not data:
                print("Stream Closed")
                raise StopIteration

            yield data
    finally:
        sd.close()


def openStream(url, quality):
    """Open a livestreamer URL and return the stream"""

    livestreamer = Livestreamer()

    try:
        streams = livestreamer.streams(url)
    except NoPluginError:
        print("Unable to Find Plugin")
        abort(404)

    except PluginError as err:
        print("Plugin error: {0}".format(err))
        abort(404)

    if quality not in streams:
        print("Quality {0} not available in {1}".format(quality, url))
        abort(404)

    return streams[quality]


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, threaded=True)
