# twitter-notifier

The present project allows the user to track some twitter accounts tweets, and periodically send an email with the content of the tweets.

# Setup

## Python 3 libraries
pip3 install twitter_scraper  

pip3 install sqlite3

pip3 install email

pip3 install smtplib


## Setting up the environment.
0- (optional) I recommend creating a new e-mail address for this project.

1- in username.txt, write the e-mail address that's going to send the e-mails.

Note: If the address domain is not gmail, you must specify the correct smtp server (smtp-mail.outlook.com for hotmail and smtp.mail.yahoo.com for yahoo in the `send()` function)

2- in password.txt, write the password

3- in followed_twitters.txt, write the usernames of the twitter accounts you want to follow. Each username occupies one line.

4- in main.py, change the address you're going to send the e-mails to (myAddr variable), and your username (subscriber variable).

5- (optional) you can change the frequency of the verification through the SLEEP_TIME variable. By default, the verification is done daily.
