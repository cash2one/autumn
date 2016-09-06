import threading
import time, datetime


def pprint():
    print 'Now:', datetime.datetime.now()
    time.sleep(2)


_thread = threading.Thread(target=pprint)
_thread.daemon = True
_thread.start()

