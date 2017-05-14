# Insta Fuck
[![GitHub license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/timgrossmann/InstaPy/blob/master/LICENSE)
[![built with Selenium](https://img.shields.io/badge/built%20with-Selenium-red.svg)](https://github.com/SeleniumHQ/selenium)
[![built with Python3](https://img.shields.io/badge/Built%20with-Python3-green.svg)](https://www.python.org/)

### Instagram Like, Comment and Follow Automation Script

Implemented in Python using the Selenium module.

#### Example

```python
from insta_core import Basic_Instagram_Core

session = Basic_Instagram_Core('login', 'password')
session.login()
session.set_restriction(max_likes=5, max_comments=50, max_follows=50)
session.get_folowers_from('anastasiya_fukkacumi', 20)
session.like_unliked(likes_per_user=3)
session.unfollow_if_time(days_to_unfollow=5)
session.end()
```

### Installation guide for windows:

#### Install python:
- Download and install newest version of python (if you do the custom install don't forget to install the pip tool)
- recommended path C:\Program Files (x86)\
> https://www.python.org/downloads/release/python-361/

#### Install Selenium
- pip install selenium

#### Download the latest chromedriver
- Download the newest chrom driver
- copy it in the folder \assets
> https://sites.google.com/a/chromium.org/chromedriver/downloads

