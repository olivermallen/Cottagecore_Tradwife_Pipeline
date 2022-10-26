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
i = 0

while True:
    try:
        print("collecting posts at time "+str(datetime.fromtimestamp(time_pointer)))
        posts=client.tagged(tag="tradblr", before=time_pointer)
        time_pointer = posts[-1]['timestamp']
        with open("pickle_files/tradblr/"+str(time_pointer)+"_"+str(i)+'.pkl', 'wb') as f:
            pickle.dump(posts, f, protocol=pickle.HIGHEST_PROTOCOL)
        str_error = None
        i = i+1
    except Exception as str_error:
        print(str_error)
        pass

    if str_error:
        time.sleep(3690)  # wait for one hour and a few seconds before trying to fetch the data again
        print("sleeping for 1 hour...")