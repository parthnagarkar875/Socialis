import tweepy
import credentials

# Part of MyStreamListener in Main.ipynb
# Streaming With Tweepy 
# Override tweepy.StreamListener to add logic to on_status

auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
auth.set_access_token(credentials.access_token, credentials.access_token_secret)    
api = tweepy.API(auth,wait_on_rate_limit=True)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # Extract info from tweets
        id_str = status.id_str
        created_at = status.created_at
        user_created_at = status.user.created_at


    def on_error(self, status_code):
        '''
        Since Twitter API has rate limits, 
        stop srcraping data as it exceed to the thresold.
        '''
        if status_code == 420:
            # return False to disconnect the stream
            return False

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)
myStream.filter(languages=["en"], track = settings.TRACK_WORDS)
