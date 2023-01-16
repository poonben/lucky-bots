import tweepy
import time

def main(event, context):
    auth = tweepy.OAuthHandler('wiMlLsl9jVP1r7vJj2NyTz76Y', 'o94r4GAdHtpG19YbvX98vtoKeaTa5nEHI10nYkHMcZ6alVxT7L')
    auth.set_access_token('1484352021499359237-8loEwvMg669hHJvVrWKHsjiho7FydL','A8BO88fmURrsYJF9JN4cgt3upd4yPD1zctXDIKVO2bxnx')

    api= tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    user = api.me()

    search = ('#slot OR #สล็อต OR #ฟรีเครดิต OR #ไม่ฝากไม่แชร์ OR @Slot OR #สล็อตฟรีเครดิต OR #เครดิตฟรีสล็อต')
    nmTweets = 100

    for tweet in tweepy.Cursor(api.search, search, lang='th').items(nmTweets):
        if not tweet.favorited:
            try:
                tweet.favorite()
                #tweet.retweet()
                time.sleep(50)
                
    #For Followback to the Followers            
    '''for follower in tweepy.Cursor(api.followers).items(1):
     if not follower.following:
        if follower.friends_count > 500:
            follower.follow()'''

            except Exception as e:
                print(e.reason)

            except StopIteration:
                break
                
