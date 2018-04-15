from tinydb import Query, TinyDB
# from os import path


class DataBase:
    def __init__(self, path):
        # if the database does not exist create new database else gets the existing tables
        self.db = TinyDB(path+'.json')
        self.blinks = self.db.table('blinks')
        self.settings = self.db.table('settings')
        self.usage = self.db.table('usage')
        self.posture = self.db.table('posture')

    def add_blinks(self, time, total):
        self.blinks.insert({'time': time, 'blinks': total})
        print(self.blinks.all())

    def write_settings(self, x, y, w, h, ran, usage):
        self.settings.insert({'x': x,
                              'y': y,
                              'width': w,
                              'height': h,
                              'range': ran,
                              'usage': usage})

    def get_settings(self):
        for tup in self.settings:
            return tup['x'], tup['y'], tup['width'], tup['height'], tup['range'], tup['usage']

    def add_posture(self, time, pose):
        self.posture.insert({'time': time,
                             'pose': pose})

    def add_usage(self, time, type, usage):
        self.usage.insert({'time': time,
                           'type': type,
                           'duration': usage})
