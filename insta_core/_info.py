"""Module used to get user info"""
from ._time import sleep
from .db_core import DB_Handler


def follower_info(browser, username):
	"""Get user info"""
	url = 'https://www.instagram.com/' + username
	if browser.current_url != url:
		browser.get(url)

	print('\n--> Getting info for -', username)
	db = DB_Handler()
	sleep(3)

	try:
		num_followers = browser.execute_script("return window._sharedData.entry_data.ProfilePage[0].user.followed_by.count")
		sleep(1)
		num_following = browser.execute_script("return window._sharedData.entry_data.ProfilePage[0].user.follows.count")
		sleep(1)
		private_check = browser.execute_script("return window._sharedData.entry_data.ProfilePage[0].user.is_private")
		sleep(1)
		media_count = browser.execute_script("return window._sharedData.entry_data.ProfilePage[0].user.media.count")
		print('Followers: {}  Following: {}  Media: {}  Private: {}'.format(num_followers, num_following, media_count, private_check))

		db.update_follower_info(username=username, is_private=private_check,
			media_count=media_count, followers=num_followers, followed=num_following)
		return private_check, media_count, num_followers, num_following
	except:
		print('Error getting user info')
		db.update_user(username=username, field='follow_count', value=-404)
