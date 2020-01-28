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

    f = generateKey(salt, masterPw)
    
    encUsername = f.encrypt(username)
    encPassword = f.encrypt(password)

    return  {
        'username': encUsername.decode("utf-8"),
        'password': encPassword.decode("utf-8"),
        'salt': salt.decode()
    }

def generateKey(salt, masterPw):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32, salt=salt,
        iterations=100000,
        backend=default_backend()
        )
    key = base64.urlsafe_b64encode(kdf.derive(masterPw))
    f = Fernet(key)
    return f

def saveConfigFile(configData, configFilename):
    #store into yaml
    stream = open(configFilename, 'w')
    dump(configData, stream)

def _decrypt(configFilename, masterPw):
    masterPw = masterPw.encode("utf-8")

    stream = open(configFilename, 'r')
    data = yaml.load(stream, Loader=yaml.FullLoader)
    username = data['username']
    password = data['password']

    #get the salt
    salt = data['salt']
    salt = salt.encode()

    f = generateKey(salt, masterPw)
    username = f.decrypt(username.encode("utf-8"))
    password = f.decrypt(password.encode("utf-8"))
    return {
        'username': username.decode("utf-8"),
        'password': password.decode("utf-8")
    }

def decrypt(masterPw):
    return _decrypt("config.yaml", masterPw)


if __name__ == "__main__":
    #prompt user for settings
    username = input("Enter Username:")
    password = input("Enter Password:")
    masterPw = input("Set Master Password:")
    encryptedData = encrypt(username, password, masterPw)
    decrypt(masterPw)
