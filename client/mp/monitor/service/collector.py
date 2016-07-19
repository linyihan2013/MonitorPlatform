from __future__ import print_function
import os

def get_pid(user, name):
    pid = os.popen('ps -u {0}|grep {1}|grep -v grep|grep -v vi|grep -v dbx \
        |grep -v tail|grep -v start|grep -v stop |sed -n 1p |awk \'{print $1}\''.format(user, name))

    return pid

if __name__ == '__main__':
    print(get_pid('root', 'rabbitmq'))