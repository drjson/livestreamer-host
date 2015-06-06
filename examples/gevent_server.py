#!/usr/bin/env python
from gevent import monkey; monkey.patch_all()
import lshost
lshost.run(server="gevent", port=5000, host="0.0.0.0")
