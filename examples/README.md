Note: To run the examples, add the src directory to your $PYTHONPATH

Simple example using built in CLI using default server.

    ./lshost.py

Simple example using built in CLI with options.

    ./lshost.py --ip "127.0.0.1" --port 8080 --server "cherrypy"

Gevent requires monkey patching applied before bottle import, so requires a custom execution script.
See: [gevent_server.py](./examples/gevent_server.py).

To run as a CGI, import and run with server set to CGI. Place the new script in your cgi-bin and set permissions.
See: [cgi_server.py](./examples/cgi_server.py).
