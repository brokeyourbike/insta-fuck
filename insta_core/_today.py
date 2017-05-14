"""Module used for showing today's ulikes users"""
from ._time import sleep


def open_lucky_one(browser, username):
	"""Open user in new tab"""

	# Open new tab
	browser.execute_script("window.open('','_blank');")
	windows = browser.window_handles
	sleep(1)
	browser.switch_to_window(windows[-1])

	# Open user
	browser.get('https://www.instagram.com/' + username)
