# This example is using Python 3
import socket
import struct

# Make a TCP socket object.
#
# API: socket(address_family, socket_type)
#
# Address family
#   AF_INET: IPv4
#   AF_INET6: IPv6
#
# Socket type
#   SOCK_STREAM: TCP socket
#   SOCK_DGRAM: UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server machine and port.
#
# API: connect(address)
#   connect to a remote socket at the given address.
server_ip = '127.0.0.1'
server_port = 8048
s.connect((server_ip, server_port))
print('Connected to server ', server_ip, ':', server_port)

# messages to send to server.


def read(message):
	i = 2
	res = '';
	length = message[0:i]
	numOfLength = struct.unpack('>h', length)[0];
	print('total number of answers is', numOfLength)
	while(numOfLength > 0):
		size = struct.unpack('>h',message[i : i + 2])[0]
		print('the length of answer', size)
		express = message[i+2 : i + 2 + size]
		s = express.decode('utf-8');
		print('the current result is', s)
		numOfLength -= 1
		i += 2 + size

	



message = [2,4, "3+12",6, "1+12/3"]
ls = []
i = 0;
while(i < len(message)):
	if(type(message[i]) == str):
		str_byte = message[i].encode('utf-8');
		ls.append(str_byte);	
	else:
		int_byte = struct.pack('>h', message[i]);		
		ls.append(int_byte);
		
	i += 1

ls.append(('\n').encode('utf-8'))
i = 0;


# Send messages to server over socket.
#
# API: send(bytes)
#   Sends data to the connected remote socket.
#   Returns the number of bytes sent. Applications
#   are responsible for checking that all data
#   has been sent
#
# API: recv(bufsize)
#   Receive data from the socket. The return value is
#   a string representing the data received. The
#   maximum amount of data to be received at once is
#   specified by bufsize
#
# API: sendall(bytes)
#   Sends data to the connected remote socket.
#   This method continues to send data from string
#   until either all data has been sent or an error
#   occurs.
bufsize = 16
size = 0
i = 0;
data = b'';

while i < len(ls):
	while size < 16:
		if i == len(ls):
			break
		data += ls[i]
		size += len(ls[i])
		i += 1

	cur = data[0:16]
	s.sendall(cur)
	data = data[16:]
	size -= 16
	print('Client sent:', cur)
 
data = s.recv(bufsize)
print('receive data: ', data)
read(data)
s.close()
  

# Close socket to send EOF to server.
