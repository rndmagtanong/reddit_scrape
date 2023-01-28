import praw
import pandas as pd
from praw.models import MoreComments
import urllib.request
import os

my_client_id = ''
my_secret = ''
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

###

subreddit = reddit_read_only.subreddit("Priconne")

# Display the name of the Subreddit
print("Display Name:", subreddit.display_name)
 
# Display the title of the Subreddit
print("Title:", subreddit.title)
 
# Display the description of the Subreddit
print("Description:", subreddit.description)

print()

###

sub_name = "Kengan_Ashura"
subreddit = reddit_read_only.subreddit(sub_name)
if not os.path.exists(sub_name):
	os.makedirs(sub_name)

# for post in subreddit.hot(limit=5):
#     print(post.title)
#     print()

###

posts = subreddit.top(time_filter = "month")
# Scraping the top posts of the current month

posts_dict = {"Title": [], "Post Text": [],
			"ID": [], "Score": [],
			"Total Comments": [], "Post URL": []
			}

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
		name = post.url.replace('https://', '')
		name = name.replace('/', '')
		path = './' + sub_name + '//' + name
		urllib.request.urlretrieve(post.url, path)
	elif post.url.endswith('.png'):
		name = post.url.replace('https://', '')
		name = name.replace('/', '')
		path = './' + sub_name + '//' + name
		urllib.request.urlretrieve(post.url, path)

# Saving the data in a pandas dataframe
top_posts = pd.DataFrame(posts_dict)
path = './' + sub_name + '//' + 'Top Posts.csv'
top_posts.to_csv(path, encoding = "utf-8", index=False)

###

# URL of the post
url = "https://www.reddit.com/r/Priconne/comments/10ldeb8/i_tried_so_hard_and_got_so_far_but_in_the_end/"
 
# Creating a submission object
submission = reddit_read_only.submission(url=url)

post_comments = []
 
for comment in submission.comments:
    if type(comment) == MoreComments:
        continue
 
    post_comments.append(comment.body)
 
# creating a dataframe
comments_df = pd.DataFrame(post_comments, columns=['comment'])
path = './' + sub_name + '//' + 'Top Comments.csv'
comments_df.to_csv(path, index=False)
