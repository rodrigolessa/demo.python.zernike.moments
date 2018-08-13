# Import the necessary packages
from zernike_moments import ZernikeMoments
from searcher import Searcher
import image_utils as iutils
import numpy as np
import argparse
import pickle as cp
import cv2
import sys
from pymongo import MongoClient

client = MongoClient('desenvolvimento', 27017)

db = client.colidencia

collection = db.figurativa

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-", "--index", required = True, help = "Path where the index file be stored")

args = vars(ap.parse_args())
 
# Load the index
index = open(args["index"], 'rb')
indexa = cp.load(index)
indexb = indexa.copy()

# Perform the search to identify the image
searcher = Searcher(indexa)

#for obj in index:
#RuntimeError: dictionary changed size during iteration

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

qt = len(indexb)

i = 1

for obj in indexb:

    # Debugging:
    #print(obj)
    #print(index[obj])

    progress(i, qt)

    # Return 30 first similarities
    results = searcher.search(indexa, indexb[obj])[:30]

    post = { "numeroProcesso": obj, "avaliado": False, "processos": [] }

    for r in results:
        #imageZeros = '{-:0>3}'.format(imageNumber)
        image_to_delete = r[1]
        image_distance = r[0]

        proc = { "numeroProcesso": image_to_delete, "similaridade": image_distance, "igual": True }

        if image_distance <= 0.011:

            post["processos"].append(proc)

            #print("Similar: {} - {}".format(image_to_delete, image_distance))
            # TODO: Write images name in a table
            # try to delete the given user, handle if the user doesn't exist.
            try:
                del indexa[image_to_delete]
            except KeyError:
                #print("{image} doesn't exist in index".format(image=image_to_delete))
                pass

        elif image_distance <= 0.051:

            post["processos"].append(proc)

            #print("barely: {} - {}".format(image_to_delete, image_distance))

    collection.insert_one(post)

    i+=1

#cv2.destroyAllWindows()