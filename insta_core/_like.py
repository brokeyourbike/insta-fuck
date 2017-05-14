"""Module used to likefeature"""
from ._time import sleep
from .db_core import DB_Handler


def like_post(browser, username, images_to_like, media_count):
	"""Find media on page and like it"""
	if images_to_like > media_count:
		images_to_like = media_count

	like_count = 0

	if images_to_like != 0:
		nodes = browser.execute_script("return window._sharedData.entry_data.ProfilePage[0].user.media.nodes")
		for i in range(images_to_like):
			browser.get('https://www.instagram.com/p/' + nodes[i]['code'])
			sleep(5)
			if like_open_image(browser):
				like_count += 1
		sleep(1)
		# browser.get('https://www.instagram.com/p/' + nodes[0]['code'])  # Open last image for like
	return like_count


def like_open_image(browser):
	"""Likes the browser opened image"""
	like_elem = browser.find_elements_by_xpath("//a[@role = 'button']/span[text()='Like']")
	liked_elem = browser.find_elements_by_xpath("//a[@role = 'button']/span[text()='Unlike']")

	if len(like_elem) == 1:
		browser.execute_script("document.getElementsByClassName('" + like_elem[0].get_attribute("class") + "')[0].click()")
		print('--> Image Liked!')
		sleep(2)
		return True
	elif len(liked_elem) == 1:
		print('--> Already Liked!')
		return False
	else:
		print('--> Invalid Like Element!')
		return False
