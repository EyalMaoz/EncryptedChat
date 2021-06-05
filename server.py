# server.py
import socket
import time
from blowfish_algo import *
import base64
from RSA import RSA_encrypt
from elsig import signMessage


print("\nWelcome to Chat Room\n")
print("Initializing....\n")
time.sleep(1)

s = socket.socket()
host = socket.gethostname()
ip = socket.gethostbyname(host)
port = 1234
s.bind((host, port))
print(host, "(", ip, ")\n")
name = 'server name'#input(str("Enter your name: "))

s.listen(1)
print("\nWaiting for incoming connections...\n")
conn, addr = s.accept()
print("Received connection from ", addr[0], "(", addr[1], ")\n")

s_name = conn.recv(1024)
s_name = s_name.decode()
print(s_name, "has connected to the chat room\nEnter [e] to exit chat room\n")
conn.send(name.encode())

# receive client's n and public key
n = int(conn.recv(1024).decode())
public_key = int(conn.recv(1024).decode())

# Blowfish key
Blowfish_key = b"admin_key"
# Send key length
key_len = len(Blowfish_key)
conn.send(str(key_len).encode())

# encrypted Blowfish key using RSA encryption with client's public key
blowfish_encrypted_key = RSA_encrypt(Blowfish_key, public_key, n)
# send encrypted Blowfish key to client
conn.send(str(blowfish_encrypted_key).encode())
print('The blowfish key i sent:',Blowfish_key)

message = b'First message'
cipher = Cipher(Blowfish_key)
encrypt_msg = b"".join(cipher.encrypt_ecb_cts(message))

# send Blowfish encrypted message to client
conn.send(encrypt_msg)
'''
while True:
    message = input(str("Me : ")).strip()
    if message == "[e]":
        message = "Left chat room!"
        conn.send(message.encode())
        print("\n")
        break

    # text = fitted text to use Blowfish with BLOW_object
    text, BLOW_object = BLOW_init(message,Blowfish_key)

    # encrypt message with Blowfish
    encrypt_msg = BLOWfish_encrypt(text, BLOW_object)
    encrypt_msg = ''.join(encrypt_msg)

    # send encrypted Blowfish key to client
    conn.send(str(encrypted_key).encode())

    # send Blowfish encrypted message to client
    conn.send(encrypt_msg.encode())

    # create and send signature to client
    signature = signMessage(encrypt_msg)
    conn.send(signature.encode())

    message = conn.recv(1024)
    message = message.decode()
    print(s_name, ":", message)

    
'''