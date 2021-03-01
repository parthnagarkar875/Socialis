import tweepy
import settings
import credentials
#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

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
