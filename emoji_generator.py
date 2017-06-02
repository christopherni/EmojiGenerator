import emoji
import json
import markovify
import praw

r = praw.Reddit('emojipasta', user_agent='emoji_pasta bot to generate titles by /u/PeachGenitals')

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
				if prevEmoji != is_emoji(c):
					words.append(text[i:j])
					prevEmoji = not prevEmoji
					i = j
				j = j + 1
			if not i:
				words.append(text)

		for word in orig_words:
			process_word(word)

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

	with open('emoji_map.json', 'w') as fp:
		json.dump(emoji_dict, fp)

try:
	emoji_dict = json.load(open('emoji_map.json', 'r'))
except FileNotFoundError:
	collect_emojis()
print(emoji_dict)