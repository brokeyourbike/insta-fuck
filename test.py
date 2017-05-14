
"""Test script"""
from insta_core import Basic_Instagram_Core

session = Basic_Instagram_Core('login', 'password')
session.login()
session.set_restriction(max_likes=5, max_comments=50, max_follows=50)
session.get_folowers_from('anastasiya_fukkacumi', 20)
session.like_unliked(likes_per_user=3)
session.unfollow_if_time(days_to_unfollow=5)
session.end()
