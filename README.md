# livestreamer-host
Simple web host for VLC (and others) to open livestreamer urls and read HTTP stream. Allows the user to add TwitchTV, etc streams to a VLC playlist as a Network Stream.

Example URL: http://localhost:5000/w/twitch.tv/monstercat/best
![Alt text](/screenshot.png?raw=true "Screenshot")

Requires:
- Python 2.7
- Livestreamer https://github.com/chrippa/livestreamer
- Flask http://flask.pocoo.org/
 
Instructions:
- Run server (./lshost.py)
- In VLC, add a new network stream to the playlist. For the URL enter http://localhost:5000/w/\<url\>/\<quality\>. Recommend setting a network buffer of atleast 1000 (the default).
- Play the desired streams. Like the CLI livestreamer, it may take a second or two to start the stream.
- The plugins and quality format are the same as the CLI arguments.

Known Issues:
- When closing VLC or stopping a stream in VLC, the server will throw an exception because the client socket has been closed. The server keeps operating normally.
