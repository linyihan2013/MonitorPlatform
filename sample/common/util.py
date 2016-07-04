'''
    Utility module
'''
from __future__ import absolute_import, division, print_function, with_statement

import hashlib
import uuid
import base64
import random

import time
import datetime

import functools

import json

from Crypto.Cipher import AES
from binascii import hexlify, unhexlify

_DATE_FORMAT_ = '%Y-%m-%d %H:%M:%S'

# _PASSWORD_ = '''23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ~!@#$^&*<>=+-_'''
_PASSWORD_ = '''23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ'''

_VERIFY_CODE_ = '1234567890'

class My_JSONEncoder(json.JSONEncoder):
    '''
        serial datetime date
    '''
    def default(self, obj):
        '''
            serialize datetime & date
        '''
        if isinstance(obj, datetime.datetime):
            return obj.strftime(_DATE_FORMAT_)
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return super(json.JSONEncoder, self).default(obj)
    

json_encoder = My_JSONEncoder(ensure_ascii=False).encode
json_decoder = json.JSONDecoder().decode

def check_codes(method):
    '''
        Decorator to check parameters.
        Encode unicode to utf-8 codes
    '''
    functools.wraps(method)
    def wrapper(*args, **kwargs):
        args = [arg.encode('utf-8', 'replace') if isinstance(arg, unicode) else arg for arg in args]
        for key,value in kwargs.iteritems():
            if isinstance(value, unicode):
                kwargs[key] = value.encode('utf-8', 'replace')
        return method(*args, **kwargs)
    return wrapper

def now(fmt=_DATE_FORMAT_, hours=0, days=0):
    '''
    '''
    now = datetime.datetime.now()
    if days or hours:
        now = now + datetime.timedelta(days=days, hours=hours)
    return now.strftime(fmt)

@check_codes
def md5(*args):
    '''
        join args and calculate md5
    '''
    md5 = hashlib.md5()
    md5.update(''.join(args))
    return md5

@check_codes
def sha1(*args):
    '''
    '''
    sha1 = hashlib.sha1()
    sha1.update(''.join(args))
    return sha1

def _fix_key(key):
    '''
        Fix key length to 32 bytes
    '''
    slist = list(key)
    fixkeys = ('*', 'z', 'a', 'M', 'h', '.', '8', '0', 'O', '.', 
               '.', 'a', '@', 'v', '5', '5', 'k', 'v', 'O', '.', 
               '*', 'z', 'a', 'r', 'h', '.', 'x', 'k', 'O', '.', 
               'q', 'g')
    if len(key) < 32:
        pos = len(key)
        while pos < 32:
            slist.append(fixkeys[pos-len(key)])
            pos += 1
    if len(key) > 32:
        slist = slist[:32]
    return ''.join(slist)

@check_codes
def aes_encrypt(data, key, mode=AES.MODE_ECB):
    '''
        Port aes encrypt from c#
    '''
    iv = '\x00'*16
    # padding input data
    encoder = PKCS7Encoder()
    padded_text = encoder.encode(data)
    key = _fix_key(key)
    cipher =  AES.new(key, mode, iv)
    cipher_text = cipher.encrypt(padded_text)
    return base64.b64encode(cipher_text)

@check_codes
def aes_decrypt(data,key, mode=AES.MODE_ECB):
    data = base64.b64decode(data)
    iv = '\x00'*16
    key = _fix_key(key)
    cipher = AES.new(key, mode, iv)
    encode_data = cipher.decrypt(data)
    encoder = PKCS7Encoder()
    chain_text = encoder.decode(encode_data)
    return chain_text

class PKCS7Encoder():
    '''
        Technique for padding a string as defined in RFC2315, section 10.3, note #2
    '''
    class InvalidBlockSizeError(Exception):
        '''
            Raise for invalid block sizes
        '''
        pass
    
    def __init__(self, block_size=16):
        if block_size < 1 or block_size > 99:
            raise self.InvalidBlockSizeError('The block size must be between 1 and 99')
        self.block_size = block_size

    def encode(self, text):
        text_length = len(text)
        amount_to_pad = self.block_size - (text_length % self.block_size)
        if amount_to_pad == 0:
            amount_to_pad = self.block_size
        pad = unhexlify('{:02x}'.format(amount_to_pad))
        return text + pad * amount_to_pad

    def decode(self, text):
        pad = int(hexlify(text[-1]))
        return text[:-pad]

