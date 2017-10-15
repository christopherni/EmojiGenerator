import emoji
import json
import markovify
import praw
import random

r = praw.Reddit('emojipasta', user_agent='emoji_pasta bot to generate titles by /u/cni5866')

emoji_dict = {}
def collect_emojis():
	global emoji_dict
	subreddit_name = "emojipasta"
	subreddit = r.subreddit(subreddit_name)

	def is_emoji(chars):
		"""Determines if char is an emoji"""
		return chars in emoji.UNICODE_EMOJI

	def process_post(text):
		prevWord = ""
		orig_words = text.split()
		words = []

		# Collects emojis and preceding word if available
		def process_word(text):
			nonlocal words
			if text.endswith(('.', '!', '?')):
				text = text[0:len(text) - 2]
			text = text.lower()
			if not text:
				return
			prevEmoji = is_emoji(text[0])
			i, j = 0, 0
			for c in text:
				if is_emoji(c):
					words.append(c)
				if prevEmoji != is_emoji(c):
					if prevEmoji:
						words.append(text[i:j])
					prevEmoji = not prevEmoji
					i = j
				j = j + 1
			if not i:
				words.append(text)

		# Processes all words + emojis
		for word in orig_words:
			process_word(word)


		# Constructs dictionary of dictionaries of frequency of emojis after words
		for word in words:
			if not is_emoji(word):
				prevWord = word
			elif prevWord:
				if prevWord in emoji_dict:
					curr = emoji_dict[prevWord]
					curr[word] = curr.get(word, 0) + 1
				else:
					emoji_dict[prevWord] = {word : 1}


	for submission in subreddit.top('all', limit=5000):
		if submission.title:
			process_post(submission.title)
		else:
			process_post(submission.selftext)

	with open('json/emoji_map.json', 'w') as fp:
		json.dump(emoji_dict, fp)

try:
	emoji_dict = json.load(open('json/emoji_map.json', 'r'))
except FileNotFoundError:
	collect_emojis()

class EmojiGenerator:
	
	def __init__(self):
		self.emoji_dict = json.load(open('json/emoji_map.json', 'r'))

	def get_emoji(self, word, prob):
		word = word.lower()
		if random.random() < prob and word in self.emoji_dict:
			emoji_possibilities = [emoj for emoj in self.emoji_dict[word] for count in range(self.emoji_dict[word][emoj])]
			return random.choice(emoji_possibilities)