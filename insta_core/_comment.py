"""Module which handles the commenting features"""
from random import choice
from ._time import sleep


def comment_post(browser, comments):
	"""Checks if it should comment on the image"""
	if do_i_commented(browser):
		return False

	rand_comment = (choice(comments))

	comment_input = browser.find_elements_by_xpath('//input[@placeholder = "Add a comment…"]')

	if len(comment_input) > 0:
		comment_input[0].send_keys(rand_comment)
		comment_input[0].submit()

	print(u'--> Commented: {}'.format(rand_comment))
	sleep(2)
	return True


def do_i_commented(browser):
	"""Check if I am already commented opened post"""
	comments = browser.execute_script(
		"return window._sharedData.entry_data.PostPage[0].graphql.shortcode_media.edge_media_to_comment.edges")
	sleep(1)
	user_to_check = browser.execute_script("return window._sharedData.config.viewer.username")
	for comment in comments:
		if user_to_check in comment['node']['owner']['username']:
			print('--> Already commented!')
			return True
		else:
			return False
