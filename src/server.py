from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from cowpy import cow


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        parsed_qs = parse_qs(parsed_path.query)

        cat = cow.Meow()
        display = cat.milk('Use /cow?msg="txt" to interact with the API')

        if parsed_path.path == '/':
            self.send_response(200)
            self.end_headers()

            self.wfile.write(b'''<!DOCTYPE html>
<html>
<head>
    <title> cowsay </title>
</head>
<body>
    <header>
        <nav>
        <ul>
            <li><a href="/cowsay">cowsay</a></li>
        </ul>
        </nav>
    <header>
    <main>
        <!-- project description -->
    </main>
</body>
</html>''')
            return

        elif parsed_path.path == '/cowsay':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(display.encode('utf-8'))
            return

        elif parsed_path.path == '/cow':
            try:
                display = cat.milk(parsed_qs['msg'][0])
                self.send_response(200)
                self.end_headers()
                self.wfile.write(display.encode('utf-8'))
                return
            except json.decoder.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'"Put your message in quotes, like this."')
                return

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        parsed_path = urlparse(self.path)
        parsed_qs = parse_qs(parsed_path.query)
        cat = cow.Meow()
        display = cat.milk('Working API?')
        post_dict = {'content': None}

        if parsed_path.path == '/cow':
            try:
                display = cat.milk(parsed_qs['msg'][0])
                post_dict['content'] = display
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(post_dict).encode('utf-8'))
                return
            except json.decoder.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(display.encode('utf-8'))
                return

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')


def create_server():
    return HTTPServer(('127.0.0.1', 3000), SimpleHTTPRequestHandler)


def run_forever():
    server = create_server()

    try:
        print('Starting server on port 3000')
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    run_forever()
