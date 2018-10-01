# This example is using Python 3
import socket
import time
import _thread
import struct

# Get host name, IP address, and port number.
host_name = socket.gethostname()
print('host_name:', host_name)
host_ip = '127.0.0.1'
host_port = 8048
print(host_ip, ':', host_port)

# Make a TCP socket object.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to server IP and port number.
s.bind((host_ip, host_port))

# Listen allow 5 pending connects.
s.listen(5)

print('\nServer started. Waiting for connection...\n')

# Limit your buffer size for send/recv API to 16 bytes.
bufsize = 16

# helper function to calculate string expr
def calculator(expr):
    l1, l2, o1, o2 = 0, 1, 1, 1
    digs = ["1","2","3","4","5","6","7","8","9","0"]
    i = 0
    while i < len(expr):
        curr = expr[i]
        if curr in digs:
            nums = curr
            while i+1 < len(expr) and expr[i+1] in digs:
                nums += expr[i+1]
                i+= 1
            num = int(nums)
            l2 = [l2 / [num,1][num==0]  , l2 * num][o2 == 1]
        elif curr == "(":
            j   = i
            cnt = 0
            while i < len(expr):
                cnt += expr[i] == "("
                cnt -= expr[i] == ")"
                if cnt == 0:
                    break
                i+=1
            num = calculator(expr[j+1:i])
            l2 = [l2 / [num,1][num==0], l2 * num][o2 == 1]

        elif curr in ["*", "/"]:
            o2 = [-1, 1][curr == '*']

        elif curr in ['+' ,'-']:
            l1 = l1 + o1 * l2
            o1 = [-1, 1][curr == '+']
            l2 = 1
            o2 = 1
        i+=1
    return (l1 + o1 * l2)

# Current time on the server.
def receive(conn):
    buff = b''
    while True:
        data = conn.recv(bufsize)
        buff += data
        if len(data) < bufsize:
            break;
    return buff

def process(buff):
    sendInfo = b''       
    total = buff[0:2]
    print('Number of answers', int.from_bytes(total, byteorder='big'))
    sendInfo += total
    start = 2
    end = 4

    while end <= len(buff):
        curLen = buff[start:end]
        length = int.from_bytes(curLen, byteorder='big')
        print('expression length is ', length)

        start = end
        end = end + length
        expression = buff[start:end]
        string = bytes.decode(expression)
        res = int(calculator(string))
        print('length of result is', len(str(res)))
        print('result is', res)
        sendInfo += struct.pack('!h', len(str(int(res))))
        sendInfo += str(int(res)).encode('utf-8')

        start = end
        end = end + 2
    return sendInfo
   

    

def mysendall(conn, ans, bufsize):
    pos = 0
    end = len(ans)
    while end > pos:
        if pos + bufsize > end:
            conn.sendall(ans[pos: end])
        else: conn.sendall(ans[pos: pos + 16])
        pos += 16

def now():
    return time.ctime(time.time())


def handler(conn):

    buff = receive(conn)
    sendInfo = process(buff)
    mysendall(conn, sendInfo, bufsize)
    

    conn.close()

while True:
    conn, addr = s.accept()
    print('Server connected by', addr,'at', now())
    _thread.start_new(handler, (conn,))

