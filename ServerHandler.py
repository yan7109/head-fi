# ServerHandler class and helper function
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import sys
import base64

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

    # Main page
    def do_HEAD(self):
        if self.path=="/":
            self.path="/index.html"

        try:
            #Open the static file requested and send it
            f = open(curdir + sep + self.path) 
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
            
    # Authentication
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Please enter the username and password:\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # Handler for the GET requests
    def do_GET(self):
        auth = False
        if self.headers.getheader('Authorization') == 'Basic ' + key:
            self.do_HEAD()
            auth = True
        else:
            self.do_AUTHHEAD()
            pass
        if auth == False:
            self.wfile.write('User not authenticated')
            return

def server_helper(port, encrypt):
    try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = HTTPServer(('', port), myHandler)
        global key
        key = encrypt
        print 'Started httpserver on port ' , port
        
        #Wait forever for incoming htto requests
        server.serve_forever()
    
    except KeyboardInterrupt:
        print '^C received, shutting down the web server'
        server.socket.close()
