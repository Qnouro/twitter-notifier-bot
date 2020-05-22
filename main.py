import sys
import sqlite3
from mailing import *
from twitter_scraper import get_tweets
from time import sleep


DATABASE = 'tweets_ids.db'
subscriber = "MyUsername"
SLEEP_TIME = 86400

def main():
    tweets_dictionary = load_dictionary()
    manage_db(tweets_dictionary)
    while True:
        try:
            print("Starting new iteration...")
            new_tweets, new_tweets_dict = verification(tweets_dictionary)
            if new_tweets:
                msg = prepare_mail(new_tweets_dict)
                send(msg, toAddr="MyEmail@gmail.com")
            print("Iteration over, sleeping...")
            sleep(SLEEP_TIME)
        except Exception as e:
            print(e)



def manage_db(tweets_dictionary):
    """
    Creates the database and initializes it.
    """
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Create table
    try:
        c.execute('''CREATE TABLE tweets(
                      user text,
                      tweet_id text,

                      UNIQUE(user, tweet_id));''')
    except Exception as e:
        print(e)

    init_db_values(c, conn, tweets_dictionary)

    conn.close()


def init_db_values(c, conn, tweets_dictionary):
    """
    Initializes the database with currently available tweets.
    """
    for user in tweets_dictionary.keys():
        tweets_list = get_tweets(user, pages=1)
        for tweet in tweets_list:
            tweet_id = tweet['tweetId']
            try:
                c.execute(f"INSERT INTO tweets VALUES (\"{user}\",{tweet_id}) ")
            except Exception as e:
                print(e)
    conn.commit()


def load_dictionary():
    """
    Returns: a dictionary containing the followed users with an empty list.
    """
    tweets_dictionary = {}
    with open("followed_twitters.txt", "r", encoding="utf-8") as twitters_file:
        for user in twitters_file.readlines():
            user = user.strip()
            tweets_dictionary[user] = []
    return tweets_dictionary


def verification(tweets_dictionary):
    """
    Verifies if new tweets were posted, and updates the dictionary accordingly.
    Returns: a boolean specifying whether new tweets were posted.
    """
    followed_users = tweets_dictionary.keys()
    update_trigger = False
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    new_tweets_dict = {}

    for user in followed_users:
        tweets_iter = c.execute(f"SELECT * FROM tweets WHERE user=\"{user}\"")
        seen_tweets = [tweet[1] for tweet in tweets_iter]
        tweets_list = get_tweets(user, pages=1)
        new_tweets = []

        for tweet in tweets_list:
            tweet_id = str(tweet['tweetId'])

            if tweet_id not in seen_tweets:
                print("New tweet!")
                update_trigger = True
                new_tweets.append(tweet['text'])
                try:
                    c.execute(f"INSERT INTO tweets VALUES (\"{user}\",{tweet_id}) ")
                except Exception as e:
                    print(e)
        conn.commit()

        new_tweets_dict[user] = new_tweets

    return update_trigger, new_tweets_dict


def prepare_mail(tweets_dictionary):
    """
    Prepares the email template containing all the new infos.
    Returns: The message to send
    """
    body = f"Hello {subscriber} ! Here are new tweets that might interest you:\n\n"

    for user in tweets_dictionary.keys():
        texts = tweets_dictionary[user]
        if texts != []:
            body += f"From {user}:\n\n"
            for text in texts:
                body += f"{text}\n\n\n"

    return message(subject="New A.I. tweets !", text=body)


if __name__ == "__main__":
    main()
