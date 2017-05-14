"""Main DB core class"""
import sqlite3
from datetime import datetime


class DB_Handler:

	def __init__(self, database='./database/data.db'):
		self.db_connect = sqlite3.connect(database)

	def create_cursor(self):
		self.cursor = self.db_connect.cursor()

	def post_commit(self):
		self.db_connect.commit()

	def post_user(self, username=None, is_private=None, media_count=None,
	 followers=None, followed=None, lang=None, follow_count=0, like_count=0,
	 comment_count=0, followed_back=None, follow_date=None):
		self.create_cursor()
		self.cursor.execute(
			"INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
				username,
				is_private,
				media_count,
				followers,
				followed,
				lang,
				follow_count,
				like_count,
				comment_count,
				followed_back,
				follow_date
			)
		)
		self.post_commit()

	def update_user(self, username, field='follow_count', value=None):
		self.create_cursor()
		self.cursor.execute(
			"UPDATE users SET {} = ? WHERE username = ?".format(field), (
				value,
				username,
			)
		)
		self.post_commit()

	def update_follower_info(self, username, is_private, media_count, followers, followed):
		self.create_cursor()
		self.cursor.execute(
			"UPDATE users SET is_private = ?, media_count = ?, followers = ?, followed = ? WHERE username = ?", (
				is_private,
				media_count,
				followers,
				followed,
				username,
			)
		)
		self.post_commit()

	def get_user(self, username):
		self.create_cursor()
		self.cursor.execute(
			"SELECT * FROM users WHERE username = ?", (
				username,
			)
		)
		return self.cursor.fetchall()

	def get_unliked_users(self, like_count=0, state='='):
		self.create_cursor()
		self.cursor.execute(
			"SELECT * FROM users WHERE like_count {} ?".format(state), (
				like_count,
			)
		)
		return self.cursor.fetchall()

	def get_followed_users(self, follow_count=0, state='>'):
		self.create_cursor()
		self.cursor.execute(
			"SELECT * FROM users WHERE follow_count {} ?".format(state), (
				follow_count,
			)
		)
		return self.cursor.fetchall()

	def update_counts(self, username, field='like_count', value=None):
		self.create_cursor()
		self.cursor.execute(
			"SELECT {} FROM users WHERE username = ?".format(field), (
				username,
			)
		)
		temp_count = self.cursor.fetchall()[0][0]
		self.create_cursor()
		self.cursor.execute(
			"UPDATE users SET {} = ? WHERE username = ?".format(field), (
				temp_count + value,
				username,
			)
		)
		self.post_commit()

	def get_comments(self):
		"""Get ALL comments"""
		self.create_cursor()
		self.cursor.execute(
			"SELECT * FROM comments", ()
		)
		return [x[0] for x in self.cursor.fetchall()]

	def get_ignore_users(self):
		"""Get ignored users"""
		self.create_cursor()
		self.cursor.execute(
			"SELECT * FROM ignore_users", ()
		)
		return [x[0] for x in self.cursor.fetchall()]

	def init_restriction(self, date=None, users='',
		likes=0, comments=0, follows=0):
		"""Init restriction"""
		if date:
			date_param = datetime.strptime(date, '%Y-%m-%d')
		else:
			date_param = datetime.now().strftime('%Y-%m-%d')
		self.create_cursor()
		self.cursor.execute(
			"INSERT INTO days VALUES (?,?,?,?,?)", (
				date_param,
				users,
				likes,
				comments,
				follows,
			)
		)
		self.post_commit()

	def get_restriction(self, date=None):
		"""Get today restriction"""
		if date:
			date_param = datetime.strptime(date, '%Y-%m-%d')
		else:
			date_param = datetime.now().strftime('%Y-%m-%d')
		self.create_cursor()
		self.cursor.execute(
			"SELECT * FROM days WHERE date_param = ?", (
				date_param,
			)
		)
		return self.cursor.fetchall()

	def update_restriction(self, date=None, field='likes', value=None):
		"""Update today restriction"""
		if date:
			date_param = datetime.strptime(date, '%Y-%m-%d')
		else:
			date_param = datetime.now().strftime('%Y-%m-%d')
		self.create_cursor()
		self.cursor.execute(
			"SELECT {} FROM days WHERE date_param = ?".format(field), (
				date_param,
			)
		)
		temp_count = self.cursor.fetchall()[0][0]
		self.cursor.execute(
			"UPDATE days SET {} = ? WHERE date_param = ?".format(field), (
				temp_count + value,
				date_param,
			)
		)
		self.post_commit()
