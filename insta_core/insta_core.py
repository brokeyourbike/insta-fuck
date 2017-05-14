"""Main core class"""
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from ._time import sleep
from ._login import login_user
from ._get import get_followers
from ._info import follower_info
from ._like import like_post
from ._today import open_lucky_one
from ._follow import follow_user, follow_back_check, follow_check
from ._comment import comment_post

from .db_core import DB_Handler


class Basic_Instagram_Core:
	def __init__(self, username=None, password=None, window_size=(400, 900)):
		"""Initialize chromedriver and aply setting"""
		chrome_options = Options()
		chrome_options.add_argument('--dns-prefetch-disable')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--lang=en-US')
		chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en-US'})
		self.browser = webdriver.Chrome('./assets/chromedriver', chrome_options=chrome_options)
		self.browser.set_window_size(window_size[0], window_size[1])
		self.browser.implicitly_wait(25)

		self.username = username
		self.password = password

		self.max_likes = 500
		self.max_comments = 50
		self.max_follows = 50

		self.db = DB_Handler()

		self.comments = self.db.get_comments()
		self.ignore_users = self.db.get_ignore_users()

		# Inialize today restriction counts
		if not self.db.get_restriction():
			self.db.init_restriction()

		self.aborting = False

	def login(self):
		"""Used to login the user either with the username and password"""
		if not login_user(self.browser, self.username, self.password):
			print('Wrong login data!')
			self.aborting = True
		else:
			print('Logged in successfully!')
		return self

	def set_restriction(self, max_likes=500, max_comments=50, max_follows=50):
		"""Set limitation for current session"""
		if self.aborting:
			return self
		self.max_likes = max_likes
		self.max_comments = max_comments
		self.max_follows = max_follows

	def get_folowers_from(self, target_user, target_count):
		"""Get followers from user, write it to DB"""
		if self.aborting:
			return self
		get_followers(self.browser, target_user, target_count)

	def like_unliked(self, likes_per_user=3):
		"""Get users with no likes and like them all"""
		if self.aborting:
			return self
		# Check if we dotn reach day LIKE limit
		if self.db.get_restriction()[0][2] < self.max_likes:
			# Get users from DB
			self.users = self.db.get_unliked_users(like_count=0, state='=')
			if self.users:
				for user in self.users:
					# Check if this user not in ignore list
					if user[0] not in self.ignore_users:
						sleep(1)
						# Get user info
						self.info = follower_info(self.browser, username=user[0])
						if self.info:
							is_private, media_count, followers, followed = self.info

							# Parametrs for chosing people
							if not is_private and (media_count > 0) and (followers < 140) and (followed > followers):

									# Like some user media
									like_count = like_post(self.browser, username=user[0],
										images_to_like=likes_per_user, media_count=media_count)
									# Write changes to DB
									self.db.update_counts(username=user[0], field='like_count', value=like_count)
									self.db.update_restriction(field='likes', value=like_count)
									if user[0] not in (self.db.get_restriction()[0][1]).split(';'):
										self.db.update_restriction(field='users', value=(str(user[0] + ';')))

	def unfollow_if_time(self, days_to_unfollow=5):
		"""Unfollow users from past"""
		if self.aborting:
			return self
		# Get users from DB
		self.users = self.db.get_followed_users(follow_count=0, state='>')
		if self.users:
			for user in self.users:
				# Check if this user not in ignore list
				if user[0] not in self.ignore_users:
					sleep(1)
					old_date = self.db.get_user(username=user[0])[0][10]
					if old_date:
						diff = (datetime.now() - datetime.strptime(old_date, '%Y-%m-%d %H:%M:%S')).days
						if diff > days_to_unfollow:
							print('--> User {} followed {} days ago'.format(user[0], diff))
							# Unfollow user
							follow_user(self.browser, username=user[0], follow=False)
							# Check for follow back
							fkc = follow_back_check(self.browser, username=user[0])
							self.db.update_user(username=user[0], field='followed_back', value=fbc)

	def check_for_following(self):
		"""Check if Iam follow someone"""
		if self.aborting:
			return self
		# Get users from DB
		self.today_users = (self.db.get_restriction()[0][1]).split(';')
		if self.today_users:
			for user in self.today_users:
				if not user:
					continue
				# Check if Iam follow user
				fc = follow_check(self.browser, user)
				if fc:
					self.db.update_counts(username=user, field='follow_count', value=1)
					self.db.update_restriction(field='follows', value=1)

	def show_today_luckies(self, num=5):
		"""Open tabs for today's lucky ones"""
		if self.aborting:
			return self
		# Get users from DB
		self.today_users = (self.db.get_restriction()[0][1]).split(';')
		if self.today_users:
			for i, user in enumerate(self.today_users, 2):
				if not user:
					continue
				# Open new tab
				open_lucky_one(self.browser, user)
				if i % num == 0:
					input('Want more?')

	def for_test(self):
		"""For test purposes ONLY"""
		# Comment last post
		if comment_post(self.browser, self.comments):
			self.db.update_counts(username=user[0], field='comment_count', value=1)

		# Follow user
		if follow_user(self.browser, username=user[0], follow=True):
			self.db.update_counts(username=user[0], field='follow_count', value=1)
			self.db.update_user(username=user[0], field='follow_date',
				value=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

	def end(self):
		"""Closes the current session"""
		self.browser.delete_all_cookies()
		self.browser.close()

		print('')
		print('Session ended')
		print('-------------')
