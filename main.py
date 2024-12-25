import socket
from io import BytesIO

import cv2
import numpy as np
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1)
    client_socket.sendto(b'\x20\x37', ("192.168.5.1", 58080))
    client_socket.sendto(b'\x20\x36', ("192.168.5.1", 58080))

    full_data = b''

    cv2.namedWindow("bebird", cv2.WINDOW_AUTOSIZE)
    while True:
        try:
            data, server = client_socket.recvfrom(1500)
            if data[4:6] == b'\xff\xd8':
                full_data = data[4:]
            elif data[-7:-5] == b'\xff\xd9':
                full_data += data[4:-5]
                try:
                    img = np.array(Image.open(BytesIO(full_data)))
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    cv2.imshow("bebird", img)
                    cv2.waitKey(1)
                except Exception as e:
                    print(e)
            else:
                full_data += data[4:]
        except socket.timeout:
            print('Socket timeout')


if __name__ == "__main__":
    main()
