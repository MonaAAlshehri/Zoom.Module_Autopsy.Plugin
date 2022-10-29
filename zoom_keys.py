#!/usr/bin/python
import dpapick3.masterkey as masterkey
import dpapick3.blob as blob
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP as Cipher_PKCS1_OAEP
from Crypto.PublicKey import RSA
from pathlib import Path
import base64
import blackboxprotobuf
import configparser
import hashlib
import os
import requests
import sys
import urllib


def usage():
    print("Usage:")
    print(
        "\t{} local  <Microsoft/Protect/SID folder> <Zoom.us.ini> <optional windows password>".format(sys.argv[0]))
    print(
        "\t{} remote [ basic/sso/google/apple ] <zoom login> <zoom password>".format(sys.argv[0]))


def main():
    remote_providers = {
        "basic": basic_login,
        "sso": sso_login,
        "google": google_login,
        "apple": apple_login
    }

    if len(sys.argv) < 2 or sys.argv[1] not in ["local", "remote"]:
        usage()
        sys.exit(1)

    if sys.argv[1] == "local":
        if len(sys.argv) != 4 and len(sys.argv) != 5:
            usage()
            sys.exit(1)

        crypto_path = sys.argv[2]
        zoomus_ini = sys.argv[3]
        if len(sys.argv) == 5:
            win_pw = sys.argv[4]
        else:
            win_pw = None

        local_key = local_decrypt(crypto_path, win_pw, zoomus_ini)
        if local_key is None:
            print("[-] Failed to decrypt local key")
        else:
            print("[*] Local key is: {}".format(local_key))

    elif sys.argv[1] == "remote":
        if len(sys.argv) != 5:
            usage()
            sys.exit(1)

        account_type = sys.argv[2]
        username = sys.argv[3]
        password = sys.argv[4]
        if account_type not in ["basic", "sso", "google", "apple"]:
            usage()
            sys.exit(1)
        print(remote_providers[account_type](username, password))


def local_decrypt(crypto_path, windows_pw, zoomus_ini):
    mkp = masterkey.MasterKeyPool()
    mkp.loadDirectory(crypto_path)
    sid = Path(crypto_path).name
    empty_password = "da39a3ee5e6b4b0d3255bfef95601890afd80709"
    if windows_pw is None:
        mkp.try_credential_hash(sid, bytes.fromhex(empty_password))
    else:
        mkp.try_credential(sid, windows_pw)

    config = configparser.ConfigParser()
    config.read(zoomus_ini)
    key = config["ZoomChat"]["win_osencrypt_key"][len("ZWOSKEY"):]
    key_blob = base64.decodebytes(key.encode("ascii"))
    dpapi_blob = blob.DPAPIBlob(key_blob)
    mks = mkp.getMasterKeys(dpapi_blob.mkguid.encode())
    for mk in mks:
        if mk.decrypted:
            dpapi_blob.decrypt(mk.get_key(), entropy=None)
            if dpapi_blob.decrypted:
                return dpapi_blob.cleartext.decode("ascii")
    return None


def basic_login(username, password):
    rand_data = os.urandom(0x20)

    def gen_cookie():
        cid = get_cid(urlencoded=True).encode("ascii")
        pubkey = \
            b"""-----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhHloLsfrcUyAtpF21GG342clr
        IopKVva8gkpw0Gr1B76QQGghLfb0/MvHg35OmxavjgXhBWa38rrH+pQ5gn1hF9QAp8vNI
        pHn5U4EshXk/CffyDV5EckQIcaxa/qxVNnqyPNUoPkaBL4tWYcgkzSFtfE7fqFnOJYuoA
        dDr3sTGGvIgY7vY7iO19mCG96WOo065L79XlGTGuOrp4y/EYdSnH+L+4u0wg15GW7nnoD
        TK9puIpF4l/KzcHXhThz1nXBRfiR1gnlxdlMs6OaYmqoKlxqas9bMWCfRnVyzFD9aymxn
        Lf8S4t7ITHWuu1mljxSm9EMPtUn0Fd157HSrvy4fQIDAQAB
        -----END PUBLIC KEY-----
        """
        input_data = hashlib.sha256(cid + rand_data).digest()
        key = RSA.importKey(pubkey)
        cipher = Cipher_PKCS1_OAEP.new(key)
        ciphertext = cipher.encrypt(input_data)
        zm_sess_key_val = urllib.parse.quote(base64.encodebytes(ciphertext)[:-1],
                                             safe="")
        return "ZM-SESS-KEY=" + zm_sess_key_val + "%2Cv1;" +\
               "srid=SaaSbeeTestMode00123578;" +\
               'zm_aid="";zm_cluster="";zm_haid="";'

    def get_cid(urlencoded=False):
        sid = "dummy"
        sid_sha = hashlib.sha256(sid.encode("ascii")).digest()
        sid_sha_twice = hashlib.sha256(sid_sha).digest()
        sid_sha_thrice = hashlib.sha256(sid_sha_twice).digest()
        result = base64.encodebytes(sid_sha_thrice)[:-1]
        if not urlencoded:
            return result
        else:
            return urllib.parse.quote(result, safe="")

    def encode_password(password):
        rand_key_hash = hashlib.sha256(
            get_cid(urlencoded=True).encode("ascii") + rand_data).digest()
        key = hashlib.sha256(rand_key_hash).digest()
        iv = hashlib.sha256(key).digest()
        BS = 16
        def pad(s): return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        cipher = AES.new(key[:0x10], AES.MODE_CBC, iv[:0x10])
        return base64.encodebytes(cipher.encrypt(pad(password).encode("ascii")))[:-1]

    sess = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (ZOOM.Win 10.0 x64)',
        'Accept': '*/*',
        'Cookie': gen_cookie(),
        'ZM-CAP': '8300585545768130487,1185289254230523812',
        'ZM-PROP': 'Win.Zoom',
        'imres': 'pc',
        'Accept-Language': 'de',
        'ZM-LOCALE': 'Def',
    }
    data = {"email": (None, username), "password": (
        None, encode_password(password))}
    req = requests.Request('POST',
                           'https://zoom.us/login?stype=100',
                           headers=headers, files=data).prepare()
    resp = sess.send(req).content
    resp_decoded = blackboxprotobuf.decode_message(resp)[0]

    email_addr = resp_decoded['5']['4'].decode("utf-8")
    first_name = resp_decoded['5']['15'].decode("utf-8")
    last_name = resp_decoded['5']['16'].decode("utf-8")
    remote_key = resp_decoded['5']['95'].decode("utf-8")
    access_token = resp_decoded['13'].decode("utf-8")
    return {"session": sess,
            "email": email_addr, "fn": first_name, "ln": last_name,
            "remote_key": remote_key, "access_token": access_token}["remote_key"]


def sso_login(username, password):
    print("[-] Not implemented")
    sys.exit(1)


def google_login(username, password):
    print("[-] Not implemented")
    sys.exit(1)


def apple_login(username, password):
    print("[-] Not implemented")
    sys.exit(1)


main()
