import socket
import cv2
import pickle
import struct

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = 'localhost'  # Replace with your own IP address or 'localhost' for testing on the same machine
    port = 9999
    socket_address = (host_ip, port)

    server_socket.bind(socket_address)
    server_socket.listen(5)

    print("Server started successfully!")

    while True:
        client_socket, addr = server_socket.accept()
        print('Got connection from', addr)
        
        if client_socket:
            vid = cv2.VideoCapture(0)
            
            while vid.isOpened():
                try:
                    img, frame = vid.read()
                    a = pickle.dumps(frame)
                    message = struct.pack("Q", len(a)) + a
                    client_socket.sendall(message)
                    
                    # cv2.imshow('Sending Video', frame)
                    # key = cv2.waitKey(1) & 0xFF
                    
                    # if key == ord('q'):
                    #     break
                except socket.error:
                    print("Client disconnected.")
                    break

    cv2.destroyAllWindows()
    server_socket.close()

if __name__ == '__main__':
    start_server()
