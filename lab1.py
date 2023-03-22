from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
import sys
from Crypto.Random import get_random_bytes
from Crypto.Cipher import  AES
from base64 import b64encode
from base64 import b64decode
import json

def derive_key(password, salt):
    return PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA256)

def encrypt(passw, salt, nonce, data):
     cipher =  AES.new(derive_key(passw, salt), AES.MODE_GCM, nonce=nonce)
     ciphertext, tag = cipher.encrypt_and_digest(bytes(data, 'utf-8'))

     json_k = ['nonce','salt', 'ciphertext', 'tag']
     json_v = [b64encode(x).decode('utf-8') for x in (cipher.nonce, salt, ciphertext, tag)]
     result = json.dumps(dict(zip(json_k, json_v)))

     return result

def decrypt(passw, json_data):
    try:
        b64 = json.loads(json_data)
        json_k = ['nonce', 'salt', 'ciphertext', 'tag']
        jv = {k: b64decode(b64[k]) for k in json_k}
        cipher = AES.new(derive_key(passw, jv['salt']), AES.MODE_GCM, nonce=jv['nonce'])
        plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
        return plaintext

    except (ValueError, KeyError):
        print("Incorrect decryption!")
        print("Wrong MasterPass or file illegaly changed")
        exit(1)

def addPass(data, newPass):
    exists = False
    if len(data) == 0:
        return newPass

    site = newPass.split(" ")

    data2 = []
    for el in data.split("\n"):
        el = el.split(" ")

        if el[0] == site[0]:
            el[1] = site[1]
            exists = True

        data2.append(el[0] + " " + el[1])

    if not exists:
        data2.append(" ".join(site))

    return '\n'.join(data2)


def findPass(data, passw):
    passw_list = data.split("\n")
    for el in passw_list:
        el = el.split(" ")

        if el[0] == passw:
            return el[1]

    return ""

if __name__ == '__main__':
    sys_args = sys.argv[1:]

    try:
        f = open("passwords.json", "r")
        file = json.load(f)
        f.close()
    except:
        file = {}

    salt = get_random_bytes(16)
    nonce = get_random_bytes(12)

    if sys_args[0] == "put" and len(sys_args) == 4:
        data = sys_args[2] + " " + sys_args[3]

        if file and len(file['ciphertext']) != 0:
            text = decrypt(sys_args[1], json.dumps(file))
            text = text.decode("utf-8")
            data = addPass(text,data)

        encrypted_json = encrypt(sys_args[1], salt, nonce, data)

        with open("passwords.json", "w") as outfile:
            outfile.write(encrypted_json)

        print("Password is stored for:", sys_args[2])


    elif sys_args[0] == "get" and len(sys_args) == 3:
        if not file or len(file['ciphertext']) == 0:
            print("trying to get a password from a empty or non existing file")
            exit(1)

        text = decrypt(sys_args[1], json.dumps(file))
        text = text.decode("utf-8")
        password = findPass(text, sys_args[2])

        if password != "":
            print("Password for", sys_args[2], "is:", password)
            exit(0)

        print("no password saved for this input")

    else:
        print("Incorrect arguments passed to the script!")
        exit(1)


