
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json
import cgi
import urlparse
import os
from urlparse import urlparse
import commands

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def broke_url(self):
        url = (self.path).split('/')
        return url

    def get_url_parameters(self):
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        return query_components

    def check_usd(self):
        output = 63
        status, output = commands.getstatusoutput("curl GET https://api.exchangeratesapi.io/latest?base=USD HTTP/1.1")
        if status == 200:
            return output['RUB']
        else:
            return output

    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        your_request = self.broke_url()
        print(self.check_usd())
        if your_request[1] == 'convert?':
            print(self.get_url_parameters())
            self.wfile.write(json.dumps({'RUB': '64', 'received': 'ok'}))
        self.wfile.write(json.dumps({'wrong': 'query', 'received': 'ok'}))



def run(server_class=HTTPServer, handler_class=Server, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print('Starting httpd on port {}...'.format(port))
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
