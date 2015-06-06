## Synopsis ##
Simple web host for VLC (and others) to open livestreamer urls and read HTTP stream. Allows the user to add TwitchTV, etc streams to a VLC playlist as a Network Stream.

### How It Works ###
Using bottle for routes, it takes a route for a path to a livestreamer source (e.g. twitch.tv/monstercat) along with the quality and opens a livestreamer session to open the stream. The stream is then returned to the client via a generator to join the bottle response and the livestreamer stream buffer.

## Example ##
An example URL added to a playlist would look like:
    
    http://localhost:5000/w/twitch.tv/monstercat/best
    
Which allows you to create playlists in VLC for quick switching between streams.
![Alt text](/screenshot.png?raw=true "Screenshot")

## Installation ##
1. Download the [source](./src/lshost.py)
2. Make the script executable.
3. (Optional) Install an alternative [server](http://bottlepy.org/docs/dev/deployment.html#server-options).

### Requires ###
- Python 2 (untested on 3)
- Livestreamer http://livestreamer.io/

         pip install livestreamer

- Bottle http://bottlepy.org/

         pip install bottle

 
## Usage ##
1. Run server

        ./lshost.py

2. In VLC, add a new network stream to the playlist. For the URL enter http://localhost:5000/w/\<url\>/\<quality\>. Recommend setting a network buffer of atleast 1000 (the default).
3. Play the desired streams. Like the CLI livestreamer, it may take a second or two to start the stream.
4. The plugins and quality format are the same as the CLI arguments for livestreamer.

To view included CLI options run with --help

    ./lshost.py --help

### Alternative Servers ###
In order to play multiple streams simultaneously you will need multithreaded support. Alternatively if running on a internal server, you may want to customize the server options.
- [Bottle Server Options](http://bottlepy.org/docs/dev/deployment.html#server-options)
- Install a WSGI server as an alternative to the built in WSGIref server if you want multithreading. Pass it to the server with the --server option.
- Supply server/port on the command line. Run `./lshost.py --help` for options.
- Wrap the bottle app in a daemon script supplying arguments and server setup to run as a service on a thin device like a pi or router running custom firmware like OpenWRT. See the [examples](./examples/).

#### Tested Servers ####
- wsgiref: Works, singlethreaded
- cherrypy: Works, multithreaded
- gevent: Works, multithreaded
- CGI: Works (uhttpd on OpenWRT)

## Known Issues ##
- Using the default servers, when closing VLC or stopping a stream in VLC, the server will throw an exception because the client socket has been closed. The server keeps operating normally.
