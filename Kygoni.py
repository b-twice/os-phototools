import os
import imghdr
import shutil
import pyexiv2
from PIL import Image, ImageFilter

class Mover(object):

    def __init__(self):
        self.home = self.get_home()
        self.photos = self.get_photos()

    def get_home(self):
        return raw_input("Which directory stores your photos? \n>>>")

    def get_photos(self):
        return [(os.path.join(dirpath, f), f) for dirpath, dirnames, files
            in os.walk(self.home) for f in files if imghdr.what(os.path.join(dirpath,f))]

    def move_photos(self):
        new_home = raw_input("Which directory to send your photos? \n>>>")
        for photo in self.photos:
            shutil.copy(photo, new_home)

class Editor(object):

    def __init__(self, home, photo):
        self.home = home
        self.photo_path = photo[0]
        self.photo_name = photo[1]
        self.photo = Image.open(photo[0])
        self.copy_path = self.replicate()

    def replicate(self):
        extension = os.path.splitext(self.photo_path)[1]
        photo_destination = os.path.join(self.home, self.photo_name + "_COPY" + extension)
        shutil.copy(self.photo_path, photo_destination)
        return photo_destination

    def crop(self, box):
        ## Will not crop unless photo is set to another variable
        output = self.photo.crop(box)
        output.save(self.photo_path)

    def blurred(self,box):
        photo_crop = self.photo.crop(box)
        for i in range(15):
            photo_crop = photo_crop.filter(ImageFilter.BLUR)
        self.photo.paste(photo_crop, box)
        self.photo.save(self.photo_path)

    def resize(self, size):
        self.photo.thumbnail(size, Image.ANTIALIAS)
        self.photo.save(self.photo_path)

    def move_exif(self):
        source_meta = pyexiv2.ImageMetadata(self.photo_path)
        source_meta.read()
        copy_meta = pyexiv2.ImageMetadata(self.copy_path)
        copy_meta.read()
        copy_meta.copy(source_meta,exif=True)
        source_meta.write()

        source_meta["Exif.Photo.PixelXDimension"] = self.photo.size[0]
        source_meta["Exif.Photo.PixelYDimension"] = self.photo.size[1]
        source_meta.write()

        os.remove(self.copy_path)

class App(object):

    def __init__ (self):
        self.actions = ['Move', 'Resize', 'Blur', 'Crop']

    def run(self):
        Storage = Mover()
        action = self.valid_action()

        if action == "Move":
            Storage.move_photos()

        if action == "Resize":
            for photo in Storage.photos:
                update = Editor(Storage.home, photo)
                size = 1200,800
                update.resize(size)
                update.move_exif()

        if action == "Blur":
            for photo in Storage.photos:
                update = Editor(Storage.home, photo)
                box = (0,0,1025,542)
                update.blurred(box)
                update.move_exif()

        if action == "Crop":
            for photo in Storage.photos:
                update = Editor(Storage.home, photo)
                box = (0,542,2590,1935)
                update.crop(box)
                update.move_exif()

    def valid_action(self):
        valid_action = False
        print 'What action would you like to perform? \n'
        for act in self.actions:
            print act
        action = raw_input("\n>>> ")
        while not (valid_action):
            if action in self.actions:
                valid_action = True
                print "Success! Your action {} is running now...".format(action)
                break
            print("Apologies, that action isn't valid. Can you say it again? \n>>> ")
        return action

if __name__ == '__main__':
    App().run()
    print "Success! I hope..."
