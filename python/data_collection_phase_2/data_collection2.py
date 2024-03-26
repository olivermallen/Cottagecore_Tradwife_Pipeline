import pytumblr2 as pytumblr
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

# convert to legacy collection to get all post bodies in html
client.npf_consumption_off()

# time_pointer starts at current time and goes back by grabbing the epoch of the last post collected

# alternate tags

time_pointer = int(time.time())

# time_pointer = int(datetime.strptime("2010-08-30 11:17:00", "%Y-%m-%d %H:%M:%S").timestamp())
i = 0

while True:  # try 4 times
    try:
        print("collecting posts at time " + str(datetime.fromtimestamp(time_pointer)))
        posts = client.tagged(tag="cottagecore", before=time_pointer)
        print(str(len(posts)) + " posts collected...")
        # print([str(datetime.fromtimestamp(post["timestamp"])) for post in posts])
        time_pointer = posts[-1]["timestamp"]
        with open(
            "/home/mel/Desktop/repos/cottagecore_tradfem_pipeline/pickle_files/collection2/"
            + str(time_pointer)
            + "_"
            + str(i)
            + ".pkl",
            "wb",
        ) as f:
            pickle.dump(posts, f, protocol=pickle.HIGHEST_PROTOCOL)
        str_error = None
        i = i + 1
    except Exception as str_error:
        print(str_error)
        print("sleeping for 1 hour...")
        time.sleep(
            3690
        )  # wait for one hour and a few seconds before trying to fetch the data again
        pass
