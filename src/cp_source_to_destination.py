import os
import shutil

# recursive function that copies all the contents
# from a source directory to a destination directory (static -> public)

# 1. should first delete all the contents of the destination (public) to ensure the copy is clean
# 2. should copy all files and subdirectories, nested files, etc.
# 3. log the path of each file copied so we can see what's happening as we run and debug the code

def cp_source_to_destination(source, destination):
    if not source or not destination:
        raise Exception("no source or destination")


    if not os.path.exists(destination):
        os.mkdir(destination)
    #print("Inside source : ", os.listdir(source))
    #print("inside destination :", os.listdir(destination))

    if len(os.listdir(destination)) > 0:
        shutil.rmtree(destination)
        os.mkdir(destination)

    for file in os.listdir(source):
        # print("file : ", file)
        pathfile = os.path.join(source, file)
        if os.path.isdir(pathfile):
            cp_source_to_destination(pathfile, os.path.join(destination, file))
        if os.path.isfile(pathfile):
            shutil.copy(pathfile, destination)
