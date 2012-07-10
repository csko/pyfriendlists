Facebook Friendlists Manager written in Python
===========

A library and command line toolkit for managing your Facebook friend lists. The friend lists are managed as sets so you can apply the well known set operations(union, intersection, difference, etc.) on them.

The library uses the [Facebook Graph API](https://developers.facebook.com/docs/reference/api/) to access and manage your [FriendLists](https://developers.facebook.com/docs/reference/api/FriendList/). Friends are added and removed using the [Batch Requests](https://developers.facebook.com/docs/reference/api/batch/).

Requirements
------------

 - Python2
 - [pyFaceGraph](https://github.com/iplatform/pyFaceGraph/)

Usage
-----

 1. [Authorize the FriendList Manager app](https://graph.facebook.com/oauth/authorize?scope=read_friendlists%2Cmanage_friendlists%2C&redirect_uri=http%3A%2F%2Fwww.facebook.com%2Fconnect%2Flogin_success.html&type=user_agent&client_id=278567538917990) so that the scripts can access and manage your Friendlists.
 2. Insert the OAuth Access token in ``friendlists.py``. You can find it as
    part of the URL of the 'Success' page after you authorize the app.
 3. See ``friendlists.py`` for example usage.


