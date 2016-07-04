''' Settings module contains all application configurations.
All configurations infomations in settings(dict type) object.
When setting module running as main module, it dumps all configurations
to cloud.conf file by pickle.'''
from __future__ import absolute_import, division, print_function, with_statement
try:
    import _pickle           # written in c
except ImportError:
    import cPickle as _pickle

import hashlib
# import wx_config
    
# import random
# import string

inf = float('inf')

# from Crypto.Cipher import AES


OUTPUT_FILE = 'serve.conf'

def md5(*args):
    m = hashlib.md5()
    data = ''.join(args)
    m.update(data)
    return m.hexdigest()

def dump():
    # Database configure

    # web application version
    settings['VERSION'] = '0.1.1'
    with open(OUTPUT_FILE, 'w') as fp:
        _pickle.dump(settings, fp)

def load():
    with open(OUTPUT_FILE, 'r') as fp:
        return _pickle.load(fp)

if __name__ == '__main__':
    dump()
    print('Dump successfully')
else:
    settings = load()
    import sys
    sys.modules[__name__] = settings

