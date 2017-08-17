# EmojiGenerator
Generates emoji pastas using Markov Chains trained using top posts from [r/emojipasta](https://www.reddit.com/r/emojipasta/). Written in Python and uses [PRAW](https://praw.readthedocs.io/en/latest/) and [Markovify](https://github.com/jsvine/markovify). Custom Markov Chain extends the base Text Markov Chain class provided in order to parse emojipastas. Custom model to choose both which words are followed by emojis and which emojis are used.

Has the following three shell commands:
* emojis get - copies one of the top emojipastas of the day to the clipboard.
* emojis gen - generates an emojipasta using a Markov Chain and copies it to the clipboard.
* emojis train - trains the Markov Chain on the day's hottest posts if it has been at least 24 hours since the last train.
