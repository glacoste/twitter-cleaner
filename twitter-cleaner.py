from keys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import os
import tweepy
import requests


def init():
    global api
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)


def main():
    init()
    count = 0
    username = api.me().screen_name
    file = open(username + "_twitter_history.txt", "w")
    images_folder = os.path.join(os.path.dirname(__file__), username + "_twitter_images")
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    for tweet in tweepy.Cursor(api.user_timeline).items():
        try:
            api.destroy_status(tweet.id)
            status_repr = str(tweet.created_at) + " " + tweet.text
            file.write(status_repr + "\n")
            count += 1

            # parse for images
            for media in tweet.entities.get("media",[{}]):
                if media.get("type", None) == "photo":
                    url = media["media_url"]
                    request = requests.get(url)
                    if request.status_code == 200:
                        filename = url.split('/')[-1]
                        with open(os.path.join(images_folder, filename), 'w+b') as image_file:
                            image_file.write(request.content)

            print("Deleted and saved: " + status_repr)
        except:
            print("Unable to delete tweet with id " + tweet.id)

    file.write("Total tweets: {0}\n".format(count))
    file.close()

if __name__ == "__main__":
    main()
