import pyttsx3
import db

global name
global screen
global func_id
global vid
global monitor_thread
global is_available
global path
global close_to
global usage_exceed
global shutdown
global database


def init():
    global engine, is_available, usage_exceed, func_id, shutdown, database
    engine = pyttsx3.init()
    is_available = False
    usage_exceed = False
    func_id = None
    shutdown = False
    database = None


class Points:
    '''Class to store points listed in the settings file'''
    x, y, w, h, range, usage = 0, 0, 0, 0, 0, 300     # static variables
    prev = 5     # corresponds to all set

