#!/usr/bin/env python

from __future__ import print_function
from bottle import route, run, abort, Response
from livestreamer import Livestreamer, StreamError, PluginError, NoPluginError

OPTIONS = {}


@route('/w/<url:path>/<quality>')
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


def setOptions(session):
    for k, v in OPTIONS.items():
        session.set_option(k, v)


def openStream(url, quality):
    """Open a livestreamer URL and return the stream"""

    livestreamer = Livestreamer()
    setOptions(livestreamer)

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
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description="Livestreamer HTTP Translation Server.")

    parser.add_argument('--ip',
                        dest='ip',
                        action='store',
                        default='0.0.0.0',
                        type=str,
                        help='IP to host on.')

    parser.add_argument('--port',
                        dest='port',
                        action='store',
                        default=5000,
                        type=int,
                        help='Port to host on.')

    parser.add_argument('--ringbuffer-size',
                        dest='ringbuffersize',
                        action='store',
                        default=16777216,
                        type=int,
                        help='Internal ring buffer size per stream in bytes.')

    parser.add_argument('--server',
                        dest='server',
                        action='store',
                        default='wsgiref',
                        type=str,
                        help="Server Backend")

    args = parser.parse_args()

    # TODO Update method for passing ring buffer size.
    OPTIONS['ringbuffer-size'] = args.ringbuffersize

    run(host=args.ip, port=args.port, server=args.server)
