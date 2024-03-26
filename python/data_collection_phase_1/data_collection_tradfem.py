import pytumblr
import time
import pickle
from datetime import datetime


keysfile = open("/home/mel/Desktop/repos/cottagecore_tradfem_pipeline/keys.txt", "r")
keys = keysfile.readlines()


client = pytumblr.TumblrRestClient(
    keys[0].strip(),
    keys[1].strip(),
    keys[0].strip(),
    keys[1].strip(),
)

# time_pointer starts at current time and goes back by grabbing the epoch of the last post collected

# alternate tags

time_pointer = int(time.time())
i = 0

while True:
    try:
        print("collecting posts at time " + str(datetime.fromtimestamp(time_pointer)))
        posts = client.tagged(tag="tradfem", before=time_pointer)
        time_pointer = posts[-1]["timestamp"]
        with open(
            "pickle_files/tradfem/" + str(time_pointer) + "_" + str(i) + ".pkl", "wb"
        ) as f:
            pickle.dump(posts, f, protocol=pickle.HIGHEST_PROTOCOL)
        str_error = None
        i = i + 1
    except Exception as str_error:
        print(str_error)
        pass

    if str_error:
        time.sleep(
            3690
        )  # wait for one hour and a few seconds before trying to fetch the data again
        print("sleeping for 1 hour...")
