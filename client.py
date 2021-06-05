# client.py
import socket
import time
import blowfish_algo as blowfish
import base64
from RSA import get_keys, RSA_decrypt
from elsig import verifyMessage
from blowfish_algo import *

'''def decrypt_msg(msg):
    msg = str.encode(msg)
    cipher_text = base64.b64decode(msg)
    plain_text = b"".join(cipher.decrypt_ecb_cts(cipher_text))
    return plain_text'''

print("\nWelcome to Chat Room\n")
print("Initializing....\n")
time.sleep(1)

s = socket.socket()
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
print(shost, "(", ip, ")\n")
host = '172.19.144.1'#input(str("Enter server address: "))
name = 'client name'#input(str("\nEnter your name: "))
port = 1234
print("\nTrying to connect to ", host, "(", port, ")\n")
time.sleep(1)
# Connect to server
s.connect((host, port))
print("Connected...\n")
# Send the server the client name
s.send(name.encode())
# Get from the server the server name
server_name = s.recv(1024).decode()
print(server_name, "has joined the chat room\nEnter [e] to exit chat room\n")

# Generate private key, public key and n for RSA
private_key, public_key, n = get_keys()
# send n and the public key to the server
s.send(str(n).encode())
s.send(str(public_key).encode())

# receive encrypted Blowfish key Size
blowfish_key_size =''
while blowfish_key_size=='':
   blowfish_key_size = s.recv(1024)
blowfish_key_size = int(blowfish_key_size.decode())

# receive encrypted Blowfish key
encrypted_blowfish_key =''
while encrypted_blowfish_key=='':
   encrypted_blowfish_key = s.recv(1024)
encrypted_blowfish_key = encrypted_blowfish_key.decode()

# decrypt the encrypted Blowfish key using RSA decryption
decrypted_blowfish_key =int.to_bytes(
    RSA_decrypt(int(encrypted_blowfish_key), private_key, n),blowfish_key_size,'big')
# Generate Cypher object to use decryption of BlowFish
cipher_object = Cipher(decrypted_blowfish_key)

#Get encrypted first message
encrypted_message = ''
while encrypted_message=='':
    encrypted_message = s.recv(1024)

decrypted_message = b"".join(cipher_object.decrypt_ecb_cts(encrypted_message))

print(decrypted_message.decode())
'''
print('The encrypted message i got:',encrypted_message)
print('The decrypted message i got:',BLOWfish_decrypt(encrypted_message,decrypted_blowfish_key.to_bytes(len("admin_key"),'big')))

'''
'''
while True:
    # receive encrypted Blowfish key
    encrypted_blowfish_key =''
    while encrypted_blowfish_key=='':
        encrypted_blowfish_key = socket.recv(1024).decode()

    # decrypt the encrypted Blowfish key using RSA decryption
    decrypted_key = RSA_decrypt(encrypted_blowfish_key, private_key, n)

    # receive the blowfish encrypted message and signature
    message = socket.recv(1024).decode()
    signature = socket.recv(1024).decode()

    # try to verify signature
    if verifyMessage(signature.split()):  # split creates an array from the signature string
        print("Message is safe")
        # decrypt blowfish encrypted message
        message =  BLOWfish_decrypt(message, decrypted_key)
        print(server_name, ":", message)
    else:
        print("Message is not safe, signature is invalid!!!!")


    message = input(str("Me : "))
    if message == "[e]":
        message = "Left chat room!"
        socket.send(message.encode(1024))
        print("\n")
        break
    socket.send(message.encode())
'''