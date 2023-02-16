import socket
import serial.tools.list_ports
import serial

serialInstance = serial.Serial("/dev/ttyACM0",9600)
serialInstance.flushInput()
serialInstance.flushOutput()


def start_server():
    print("Starting Server...")
    host = ''
    port = 12345
    
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # inshallah this response error will be solved, allah bless
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to a specific address and port
    server_socket.bind((host, port))
    
    # Start listening for incoming connections
    server_socket.listen(1)
    print("Server listening on {}:{}".format(host, port))
    
    while True:
        # Accept an incoming connection
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from {}".format(client_address))
        serialInstance = serial.Serial("/dev/ttyACM0",9600)
        print("Port /dev/ttyACM0 opened...")
        serialInstance.flushInput()
        serialInstance.flushOutput()

        while True:
            data = client_socket.recv(16)
    
            if data:
                message = data.decode('utf-8')
                print ("Received:",message)
                
                response = "Received:" + message
                client_socket.sendall(response.encode('utf-8'))
                serialInstance.write(message.encode())
                if message == "exit":
                    break
                
            else:
                print("wah wah")
                break
        
        # Close the connection with the current client
        client_socket.close()
        print("Closed connection with {}".format(client_address))
        serialInstance.close()
        print("Port /dev/ttyACM0 closed...")

if __name__ == "__main__":
    start_server()
