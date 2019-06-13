#!/usr/bin/python3

import sys

import logging

logging.basicConfig(stream=sys.stderr)

sys.path.insert(0,'/var/www/GPStuy/')



from GPStuy import app as application 

