
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json
import cgi
from urlparse import urlparse
import urllib2


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
        html = 63
        url= ("https://api.exchangeratesapi.io/latest?base=USD")
        try:
            response = urllib2.urlopen(url)
            html = json.load(response)
        except:
            pass
            return html
        return html['rates']['RUB']



    def do_GET(self):
        self._set_headers()
        your_request = self.broke_url()
        if your_request[1] == 'convert':
            parameters = self.get_url_parameters()
            try:
                usd = int(round(float(parameters["Amount"])))
            except ValueError:
                return self.wfile.write(json.dumps({'wrong': 'amount', 'received': 'error'}))
            if type(usd) == int:
                rub_couse = self.check_usd()
                res = usd*rub_couse
                self.wfile.write(json.dumps({"converted":"USD_TO_RUB", "USD":usd, 'RUB': res, 'received': 'ok'}))
        else:
            self.wfile.write(json.dumps({'wrong': 'query', 'received': 'error'}))



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
