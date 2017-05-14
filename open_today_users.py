
"""Script """
import webbrowser
from insta_core import DB_Handler
from insta_core import Basic_Instagram_Core

db = DB_Handler()


def show_today_luckies(num=5):
	"""Open tabs for today's lucky ones"""

	# Get users from DB
	today_users = (db.get_restriction()[0][1]).split(';')
	if today_users:
		for i, user in enumerate(today_users):
			if not user:
				continue
			# Open new tab
			url = 'https://www.instagram.com/' + user
			webbrowser.open(url)
			if i % num == 0:
				input('-- Want more?')


def check_for_following():
	session = Basic_Instagram_Core('login', 'password')
	session.login()
	session.check_for_following()
	session.end()


if __name__ == '__main__':
	show_today_luckies()
	while True:
		inp = input('\n-- Type "yes" to start CHECK: ')
		if str(inp) == 'yes':
			check_for_following()
		else:
			break
