import http.server as server
import socketserver as socket
import os

# create function to start server 
def start_server():
    # Ask for the server port
    port = int(input('Enter the server port: '))

    # Ask for the server host
    host = input('Enter the server host: ')

    # Define the server address
    address = (host, port)

    # Create a function to handle http requests
    handler = server.SimpleHTTPRequestHandler

    # Create a function to respond and start
    resp = socket.TCPServer(address, handler)

    # Execute the server start
    try:
        os.system("cls")
        print(f'Server opened the link : http://{host}:{port}/')
        resp.serve_forever()
    except KeyboardInterrupt:
        print('Server closed')
        
start_server()