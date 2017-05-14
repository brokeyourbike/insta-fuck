"""Module used for follow feature"""
from ._time import sleep


def follow_user(browser, username, follow=True):
	"""Follows the user of the currently opened image"""
	is_followed = follow_check(browser, username)

	if follow and not is_followed:
		follow_button = browser.find_element_by_xpath("//*[contains(text(), 'Follow')]")
		follow_button.click()
		print('--> Now following')
		sleep(3)
		return True
	elif not follow and is_followed:
		unfollow_button = follow_button = browser.find_element_by_xpath("//*[contains(text(), 'Following')]")
		unfollow_button.click()
		print('--> Now Unfollowing')
		sleep(3)
		return True
	else:
		print('--> Already done.')
		sleep(1)
		return False


def follow_back_check(browser, username):
	"""Check if user follow me back"""
	url = 'https://www.instagram.com/' + username
	if browser.current_url != url:
		browser.get(url)
	sleep(2)
	follow_back = browser.execute_script("return window._sharedData.entry_data.ProfilePage[0].user.follows_viewer")

	if follow_back:
		return True
	else:
		return False


def follow_check(browser, username):
	"""Check if Iam follow user"""
	url = 'https://www.instagram.com/' + username
	if browser.current_url != url:
		browser.get(url)
	sleep(2)
	is_followed = browser.execute_script("return window._sharedData.entry_data.ProfilePage[0].user.followed_by_viewer")
	return is_followed
