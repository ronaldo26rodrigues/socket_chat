import http.server
import socketserver

HOST = ""
PORT = 8080

Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer((HOST, PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()