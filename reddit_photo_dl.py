import praw
import urllib.request
import os

def initialize_instance():
	my_client_id = 'vrmDfDh2BCQtlBqZjwyXlA'
	my_secret = '8vGLp6NHfR1uMeqC6JPkR0eLQjQfwg'
	my_user_agent = 'Scraping'

	# Read-only instance
	reddit_read_only = praw.Reddit(client_id = my_client_id,         # your client id
		client_secret = my_secret,                                   # your client secret
		user_agent = my_user_agent)                                  # your user agent
	
	# Authorized instance
	reddit_authorized = praw.Reddit(client_id="",                    # your client id
		client_secret="",                                            # your client secret
		user_agent="",                                               # your user agent
		username="",                                                 # your reddit username
		password="")                                                 # your reddit password
	
	return reddit_read_only, reddit_authorized

###

def scrape(reddit_read_only, sub_name):
	subreddit = reddit_read_only.subreddit(sub_name)
	if not os.path.exists(sub_name):
		print("Creating folder...")
		os.makedirs(sub_name)
	else:
		print("Directory already exists. Continuing...")

	###

	posts = subreddit.top(time_filter = "all", limit = 50)
	# Scraping the top posts of all time

	posts_dict = {"Title": [], "Post Text": [],
				"ID": [], "Score": [],
				"Total Comments": [], "Post URL": []
				}

	# Look through the posts

	print("Beginning to download photos...")

	count = 0
	for post in posts:
		# Title of each post
		posts_dict["Title"].append(post.title)
		
		# Text inside a post
		posts_dict["Post Text"].append(post.selftext)
		
		# Unique ID of each post
		posts_dict["ID"].append(post.id)
		
		# The score of a post
		posts_dict["Score"].append(post.score)
		
		# Total number of comments inside the post
		posts_dict["Total Comments"].append(post.num_comments)
		
		# URL of each post
		posts_dict["Post URL"].append(post.url)
		if post.url.endswith('.jpg'):
			name = post.url.split("/")[-1]
			path = './' + sub_name + '//' + name
			urllib.request.urlretrieve(post.url, path)
			count += 1
		elif post.url.endswith('.png'):
			name = post.url.split("/")[-1]
			path = './' + sub_name + '//' + name
			urllib.request.urlretrieve(post.url, path)
			count += 1

	print('Downloaded ' + str(count) + ' photos.')
	print('Bye!')

if __name__ == "__main__":
	print("Enter subreddit to scrape: ")
	sub_name = input()
	reddit_read_only, reddit_authorized = initialize_instance()
	scrape(reddit_read_only, sub_name)