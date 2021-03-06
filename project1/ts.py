import sys
import threading
import time
import random

import socket

DNS_table = dict();


def topserver(port):
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print("socket open error: ()\n".format(err))
        exit()

    server_binding = ('', port)
    ss.bind(server_binding)
    ss.listen(1)

    while True:
        conn, addr = ss.accept();
        revbuf = "";

        while True:
            try:
                data = conn.recv(1024);

                if data == b"":
                    break;
                revbuf += data;

                try:
                    while True:
                        pos = revbuf.find('\n')

                        if pos < 0:
                            break;

                        if pos > 0:
                            domain = revbuf[0:pos].replace(' ', '').replace('\r', '');
                            revbuf = revbuf[pos + 1:]

                            if DNS_table.has_key(domain.lower()):
                                conn.send(domain + " " + DNS_table[domain.lower()] + " A\n")
                            else:
                                conn.send(domain + " - Error:HOST NOT FOUND\n")
                except:
                    {

                    }
            except socket.error as e:
                break;

        conn.close()


if __name__ == "__main__":
    try:
        with open("PROJI-DNSTS.txt", "r") as f:
            for line in f:
                arr = line.replace('\r', '').replace('\n', '').split(' ');

                if len(arr) == 3:
                    if arr[2] == "A":
                        DNS_table[arr[0].lower()] = arr[1]

        topserver(int(sys.argv[1]))
    except:
        {

        }