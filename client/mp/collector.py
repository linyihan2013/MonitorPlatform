from __future__ import print_function

import time
import cpu1
import cpu2
import disk
import interface
import mem


def run():
    print("hello test service %s \r\n" % str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    cpu1.output()
    cpu2.output()
    mem.output()
    disk.output()
    interface.output()

if __name__ == '__main__':
    run()