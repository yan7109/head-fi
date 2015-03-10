# Invoking main program

#!/usr/bin/python
import sys
import base64
from ServerHandler import *

if (len(sys.argv)<3) or (':' not in sys.argv[2]) or (not (sys.argv[1]).isdigit()) or (int(sys.argv[1])<8000):
    print "Usage: python main.py [port>=8000] [username:password]"
    sys.exit()
    
encrypt = base64.b64encode(sys.argv[2])
port = int(sys.argv[1])

server_helper(port, encrypt)


