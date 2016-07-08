''' Settings module contains all application configurations.
All configurations infomations in settings(dict type) object.
When setting module running as main module, it dumps all configurations
to cloud.conf file by pickle.'''
from __future__ import absolute_import, division, print_function, with_statement

try:
    import _pickle  # written in c
except ImportError:
    import cPickle as _pickle

OUTPUT_FILE = 'server.conf'

def dump():
    # Database configure
    settings = {}
    settings['MONGODB_DBNAME'] = 'idc'
    settings['MONGODB_USER'] = 'mp'
    settings['MONGODB_PASSWORD'] = 'mp_LYH_001*'
    settings['MONGODB_IP'] = '14.23.62.180'
    settings['MONGODB_PORT'] = '27517'

    # web application version
    settings['VERSION'] = '0.1'
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