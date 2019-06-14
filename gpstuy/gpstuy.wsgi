#!/usr/bin/python3

import sys

import logging

logging.basicConfig(stream=sys.stderr)

sys.path.insert(0,'/var/www/gpstuy/')



from gpstuy import app as application 

