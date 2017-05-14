"""Module for geting new followers"""
from ._time import sleep
from .db_core import DB_Handler


def get_followers(browser, username, target_count):
	url = 'https://www.instagram.com/' + username
	if browser.current_url != url:
		browser.get(url)

	print('\n## Getting followers from - ', username)

	follow_link = browser.find_element_by_partial_link_text('followers')
	follow_link.click()

	table_of_followers = browser.find_elements_by_tag_name('li')

	while len(table_of_followers) < target_count:
		table_of_followers = browser.find_elements_by_tag_name('li')
		print('.', end='')
		browser.execute_script("window.scrollBy(0, document.body.scrollHeight)")
		sleep(0.1)
	print('\n')

	db = DB_Handler()
	users_geted = 0

	for i in range(len(table_of_followers) - 12):  # last 12 elements always error
		try:
			elem = table_of_followers[i].find_elements_by_tag_name('a')[1]
			print('Writing to DB -', elem.text)
			if not db.get_user(username=elem.text):
				db.post_user(username=elem.text)
				users_geted += 1
		except:
			print('Error geting element')
	print('## Get {} users\n'.format(users_geted))
	return users_geted
