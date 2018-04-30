import tweepy
import time
import markovify
import pronouncing
import random

# set up twitter bot access and tweet function
class TwitterAPI:
  def __init__(self):
    consumer_key = ''
    consumer_secret = ''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    access_token = ''
    access_secret = ''
    auth.set_access_token(access_token, access_secret)
    self.api = tweepy.API(auth)
    
  def tweet_function(self,verse):
    self.api.update_status(verse)
    print verse   

# set up markovify, create variables
with open("heart_darkness.txt") as f:
  text = f.read()
text_model = markovify.Text(text)
api = TwitterAPI()

first_line = " "
second_line = " "
third_line = " "
fourth_line = " "

last_word = " "
last_word2 = " " 
rhymes = []
hashtags = ["#RawPoetry", "#DeepPoems", "#SpittingBars", "#Verses", "#RhymingSimon", "#ABCB", "#PoetryVibes", "#SimpleWordPlay", "#HoD", "#HeartOfDarkness", "#InspiredPoet"]


# generate a new four lines
j = True
while j:

  # generate random words for lines 1 and 3
  first_line = text_model.make_short_sentence(60)
  third_line = text_model.make_short_sentence(60)

  #generate either one or two hashtags
  random1 = random.randint(0,10)
  hashtag1 = hashtags[random1]
  hashtag2 = ' '
  i = True
  if random1 > 4:
    while i:
      random2 = random.randint(0,10)
      if random1 != random2:
        hashtag2 = hashtags[random2]
        i = False
      else: 
        continue
  
  # generate the second line, grab last word, and find the words that rhyme with it
  i = True
  while i:
    second_line = text_model.make_short_sentence(60)
    if first_line is None:
      continue
    last_word = second_line.split()[-1]
    last_word = last_word[:-1]
    rhymes = pronouncing.rhymes(last_word)
    if len(rhymes) > 18:
      break
  rhymes = [x.encode('utf8') for x in rhymes]  

  #generate the fourth line, grab the last word, and see if it matches with any rhymes
  timeout = time.time() + 20
  i = True
  while i:
    fourth_line = text_model.make_short_sentence(60)
    if fourth_line is None:
      continue
    last_word2 = fourth_line.split()[-1]
    last_word2 = last_word2[:-1]
    
    # match last word to rhymes. if it pairs, send the verse to publish it
    for word in rhymes:
      if word == last_word2:
        verse = first_line + '\n' + second_line + '\n' + third_line + '\n' + fourth_line + '\n' + hashtag1 + ' ' + hashtag2
        api.tweet_function(verse)
        time.sleep(60)
        i = False
        #j = False
        break

    # if it takes > 20 secs to find a sentence that rhymes, redo the entire verse
    if time.time() > timeout:
      time.sleep(6)
      break




