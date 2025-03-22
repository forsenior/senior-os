import hashlib
import os
import pathlib
import secrets
import struct
from random import randint

from Crypto.Cipher import AES
import uuid
import random



KEY_DIR = "/", "persistence", "keys"

# Check existance of keydir storage
def keydir_exist():
    if pathlib.Path(os.path.join(*KEY_DIR)).exists():
        return True
    return False

# Checks whether the machine key exists
def machine_key_exists():
    mac = uuid.getnode().to_bytes(6)
    h = hashlib.sha3_384()
    h.update(mac)
    filename = h.hexdigest()
    if pathlib.Path(os.path.join(*KEY_DIR, f"{filename}")).exists():
        return True
    return False

# Creates the keys dir
def create_keys_dir():
    if not keydir_exist():
        os.makedirs(os.path.join(*KEY_DIR))

def master_key_exist():
    if pathlib.Path(os.path.join(*KEY_DIR, "master_key")).exists():
        return True
    
def create_master_key(password):
    if not keydir_exist():
        create_keys_dir()
    if not master_key_exist():
        master_key = secrets.token_bytes(32)
        salt = secrets.token_bytes(4)
        iterations = random.randint(600000,700000)
        kdf = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), salt, iterations)
        cipher = AES.new(kdf, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(master_key)
        with open(os.path.join(*KEY_DIR, "master_key"), "wb") as master_key_file:
            packed = struct.pack("@4si16s32s16s",salt, iterations, nonce, ciphertext, tag)
            master_key_file.write(packed)
            master_key_file.flush()

def read_master_key(password):
    if not master_key_exist():
        create_master_key(password)
    with open(os.path.join(*KEY_DIR, "master_key"), "rb") as master_key_file:
        salt, iterations, nonce, ciphertext, tag = struct.unpack("@4si16s32s16s", master_key_file.read())
    kdf = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), salt, iterations)
    cipher = AES.new(kdf, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        print("Master key deciphered.")
    except ValueError:
        print("Key incorrect or message corrupted")
        return None
    return plaintext

# Allows adding new machine keys into the config file
def create_machine_key(password):
    master_key = read_master_key(password)
    salt = secrets.token_bytes(4)
    iterations = random.randint(600000,700000)
    mac = uuid.getnode().to_bytes(6)
    kdf = hashlib.pbkdf2_hmac('sha256', mac, salt, iterations)
    cipher = AES.new(kdf, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(master_key)
    h = hashlib.sha3_384()
    h.update(mac)
    filename = h.hexdigest()
    with open(os.path.join(*KEY_DIR, filename), "wb") as master_key_file:
        packed = struct.pack("@4si16s32s16s", salt, iterations, nonce, ciphertext, tag)
        master_key_file.write(packed)
        master_key_file.flush()

# Injects key into config read and config write
def read_machine_key():
    if not machine_key_exists():
        raise KeyError("Machine key not found. Create new!")
    mac = uuid.getnode().to_bytes(6)
    h = hashlib.sha3_384()
    h.update(mac)
    filename = h.hexdigest()
    with open(os.path.join(*KEY_DIR, filename), "rb") as master_key_file:
        salt, iterations, nonce, ciphertext, tag = struct.unpack("@4si16s32s16s", master_key_file.read())
    kdf = hashlib.pbkdf2_hmac('sha256', mac, salt, iterations)
    cipher = AES.new(kdf, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        print("Machine key deciphered.")
    except ValueError:
        print("Key incorrect or message corrupted")
        return None
    return plaintext

# Reads and decrypts the configuration file
def read_config():
    key = read_machine_key()
    with open(os.path.join('/','persistence','config'), "rb") as config_file:
        nonce = config_file.read(16)
        tag = config_file.read(16)
        cryptogram = config_file.read()
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(cryptogram)
    try:
        cipher.verify(tag)
        print("Config deciphered")
    except ValueError:
        print("Key incorrect or config corrupted")
        return None
    return str(plaintext, 'utf-8')

# Writes and encrypts the configuration
def write_config(config: str):
    key = read_machine_key()
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(bytes(config, 'utf-8'))
    with open(os.path.join('/','persistence','config'), "wb") as config_file:
        config_file.write(nonce)
        config_file.write(tag)
        config_file.write(ciphertext)
        config_file.flush()

def main():
    pass


if __name__ == '__main__':
    main()