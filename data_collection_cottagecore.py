import pytumblr
import time
import pickle
from datetime import datetime



client = pytumblr.TumblrRestClient(
    '***REMOVED***',
    '***REMOVED***',
    '***REMOVED***',
    '***REMOVED***',
)

#time_pointer starts at current time and goes back by grabbing the epoch of the last post collected

#alternate tags

time_pointer = int(time.time())
time_pointer = int(datetime.strptime("2022-04-13 00:10:15", "%Y-%m-%d %H:%M:%S").timestamp())
i = 0

while True:  # try 4 times
    try:
        print("collecting posts at time "+str(datetime.fromtimestamp(time_pointer)))
        posts=client.tagged(tag="cottagecore", before=time_pointer)
        time_pointer = posts[19]['timestamp']
        with open("pickle_files/cottagecore/"+str(time_pointer)+"_"+str(i)+'.pkl', 'wb') as f:
            pickle.dump(posts, f, protocol=pickle.HIGHEST_PROTOCOL)
        str_error = None
        i = i+1
    except Exception as str_error:
        print(str_error)
        print("sleeping for 1 hour...")
        time.sleep(3690)  # wait for one hour and a few seconds before trying to fetch the data again
        pass
