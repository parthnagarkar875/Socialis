from typing_extensions import final
import tweepy
import settings
import credentials
#override tweepy.StreamListener to add logic to on_status


class MyStreamListener(tweepy.StreamListener):


    def get_full_text(self, status):
        final_text=str()

        # Get full text from a tweet
        try:
            if hasattr(status, 'retweeted_status') and hasattr(status.retweeted_status, 'extended_tweet'):
                final_text=status.retweeted_status.extended_tweet['full_text']
                # print("Extended Tweet:", status.retweeted_status.extended_tweet['full_text'])
            elif hasattr(status, 'extended_tweet'):
                final_text=status.extended_tweet['full_text']
                # print("Extended Tweet:", status.extended_tweet['full_text'])                
            else:
                final_text=status.text
                # print("Printing Full text", status.text)
        except AttributeError as e:
            pass
        
        return final_text

    def on_status(self, status):
        final_text=self.get_full_text(status)
        if final_text[:2] != 'RT':
            print("https://twitter.com/"+status.user.screen_name+"/status/"+status.id_str, "\t", status.favorite_count)
            # print(final_text)

auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
auth.set_access_token(credentials.access_token, credentials.access_token_secret)    
api = tweepy.API(auth,wait_on_rate_limit=True)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener, tweet_mode='extended')

try:
    myStream.filter(languages=["en"], track = settings.TRACK_WORDS)
except Exception as e:
    print("Error. Restarting Stream.... Error: ")
    print(e.__doc__)
    print(e.message)





# import multiprocessing
# import os
# from time import sleep
# import threading 
# import time


# def odd(msg):
#     print("Executing our P1 Task with {} on Process: {}".format(msg, os.getpid()))    
#     for i in range(1,10,2):
#         print("Odd number: ",i)
                

# def even():
#     print("Executing our p2 Task on Process: {}".format(os.getpid()))
#     # sleep(5)
#     for i in range(2,10,2):
#         print("Even number: ",i)


# if __name__ == "__main__": 

#     start_time = time.time()
   
#     p1 = multiprocessing.Process(target=odd, args=("In Process",)) 
#     p2 = multiprocessing.Process(target=even) 

#     # t1 = threading.Thread(target=odd, args=("In Process",)) 
#     # t2 = threading.Thread(target=even) 

#     # starting process 1 
#     p1.start() 
#     # starting process 2 
#     p2.start() 
#     odd("Out of Process")
#     # wait until process 1 is finished 
#     # p1.join() 
#     # wait until process 2 is finished 
#     p1.join()
#     p2.join() 

#     # both processes finished 
#     print("Done!") 
#     print("--- %s seconds ---" % (time.time() - start_time))
