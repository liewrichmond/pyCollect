import base64
import os
import yaml
import sys
from base64 import b64encode
from yaml import load, dump
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def encrypt(username, password, masterPw):
    #encode to bytearr
    username = username.encode("utf-8")
    password = password.encode("utf-8")
    masterPw = masterPw.encode("utf-8")

    #configurations for crypto library
    salt = os.urandom(16)
    salt = b64encode(salt)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32, salt=salt,
        iterations=100000,
        backend=default_backend()
        )
    key = base64.urlsafe_b64encode(kdf.derive(masterPw))

    #encode
    f = Fernet(key)
    encUsername = f.encrypt(username)
    encPassword = f.encrypt(password)

    #store into yaml
    stream = open('config.yaml', 'w')
    yamlOutput = {
        'username': encUsername.decode("utf-8"),
        'password': encPassword.decode("utf-8"),
        'salt': salt.decode()
    }
    dump(yamlOutput, stream)

def decrypt(masterPw):
    stream = open('config.yaml', 'r')
    data = yaml.load(stream, Loader=yaml.FullLoader)
    print(data['username'])

if __name__ == "__main__":
    #prompt user for settings
    username = input("Enter Username:")
    password = input("Enter Password:")
    masterPw = input("Set Master Password:")
    encrypt(username, password, masterPw)
    decrypt(masterPw)
