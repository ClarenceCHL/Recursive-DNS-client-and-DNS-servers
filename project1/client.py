import socket
import sys

def sendDNSrequest(socket,domain):
    revbuf = ""
    result = "";
    socket.send(domain + "\n")
    recvok = False

    while not recvok:
        try:
            data = socket.recv(1024);

            if data == b"":
                break;
            revbuf += data;

            try:
                while True:
                    pos = revbuf.find('\n')

                    if pos < 0:
                        break;

                    if pos > 0:
                        result = revbuf[0:pos].replace('\n', '').replace('\r', '')
                        recvok = True
                        break;

            except:
                {

                }
        except:
            {

            }

    return result;

if __name__ == "__main__":
    try:
        rshost = sys.argv[1]
        rsport = int(sys.argv[2])
        tsport = int(sys.argv[3])
        rssocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        rssocket.connect((rshost,rsport))

        with open("PROJI-HNS.txt", "r") as f:
            with open("RESOLVED.txt","w") as fout:
                for line in f:
                    try:
                        domain = line.replace('\r', '').replace('\n', '');
                        result = sendDNSrequest(rssocket,domain).replace('\r', '').replace('\n', '')

                        arr = result.split(' ')
                        ip = arr[0]

                        if arr[2] == "NS":
                            tssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            tssocket.connect((ip,tsport))
                            result = sendDNSrequest(tssocket,domain)
                            tssocket.close()
                            arr = result.split(' ')
                            ip = arr[0]

                        fout.write(result + "\n")
                    except Exception as e:
                        {

                        }

        rssocket.close()

    except Exception as e:
        {

        }