import socket
import pickle
import struct
import cv2

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = 'localhost'  # Replace with the server IP address or 'localhost' if running the server on the same machine
    port = 9999
    socket_address = (host_ip, port)

    client_socket.connect(socket_address)
    data = b""
    payload_size = struct.calcsize("Q")

    while True:
        try:
            while len(data) < payload_size:
                packet = client_socket.recv(4*1024)  # 4KB buffer size
                if not packet:
                    break
                data += packet

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4*1024)

            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)

            cv2.imshow("Received Video", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break
        except socket.error:
            print("Server disconnected.")
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    start_client()
