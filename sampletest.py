import tweepy
import settings
import credentials
#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

# auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
# auth.set_access_token(credentials.access_token, credentials.access_token_secret)    
# api = tweepy.API(auth,wait_on_rate_limit=True)

# myStreamListener = MyStreamListener()
# myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener, tweet_mode='extended')

# try:
#     myStream.filter(languages=["en"], track = settings.TRACK_WORDS)
# except Exception as e:
#     print("Error. Restarting Stream.... Error: ")
#     print(e.__doc__)
#     print(e.message)

import multiprocessing
import os
from time import sleep

class hello:
    def odd():
        print("Executing our Task on Process: {}".format(os.getpid()))    
        for i in range(1,10,2):
            print("Odd number: ",i)
                    

    def even():
        print("Executing our Task on Process: {}".format(os.getpid()))
        sleep(5)
        for i in range(2,10,2):
            print("Even number: ",i)


if __name__ == "__main__": 
    a=hello()
    p1 = multiprocessing.Process(target=hello.odd) 
    p2 = multiprocessing.Process(target=hello.even) 

    # starting process 1 
    p1.start() 
    # starting process 2 
    p2.start() 

    # wait until process 1 is finished 
    p1.join() 
    # wait until process 2 is finished 
    p2.join() 

    # both processes finished 
    print("Done!") 