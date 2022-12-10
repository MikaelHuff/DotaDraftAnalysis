import os
import shutil
import dataComp as data

# Takes a folder "heroes" that contains many images (heroes + other characters in the game
# that are not playable), and finds the ones that match the playable heroes and moves them
# into a different folder "Images" to be used for the GUI. Made this as the the official
# download for the images had more images than required
# NOTE: This only needs to be run if the Images folder is empty or missing heroes.

data = data.data()
heroNames = data.getHeroList()
# get the path/directory
folder_start = "heroes"
folder_dest = "Images"
for image in os.listdir(folder_start):
    # check if the image ends with png
    if (image.endswith(".png")):
        length = len(image)
        imageName = image[0:length-4]
        if heroNames.count(imageName):
            num = heroNames.index(imageName)
            shutil.copy(folder_start+'\\'+image,folder_dest+'\\'+image)
            print(imageName)
        if image == 'default.png':
            shutil.copy(folder_start+'\\default.png',folder_dest+'\\default.png')
            print(imageName)
