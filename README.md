avatars-io-python
=================

Python avatar picker and uploader for Avatars.io.

Current version of **avatarsio** is **0.1**; it's stable.

Requirements, dependencies
--------------------------

`avatarsio` supports both Python 2 and Python 3 and is on
[PyPi](http://pypi.python.org/pypi/avatarsio/).

As described in `requirements.txt`, the only dependency is
[`requests`](http://docs.python-requests.org) (HTTP for humans, because, well,
it is awesome and should be built-in).

You can install it from source or using `pip` (eg. in a virtualenv):

    pip install avatarsio

Usage
-----

You don't really need the lib if you just want to get user avatars from
services such as Twitter of Facebook. Just use the corresponding URL as
explained on [avatars.io](http://avatars.io/).

The lib is useful for custom avatar upload. You need first to
[register an app](http://apps.getchute.com/apps/new) on Chute. Then, it's quite
straightforward:

```python
>>> from avatarsio import AvatarsIO
>>> avtio = AvatarsIO('my-client-id', 'my-access-token')

# With a file name:
>>> avtio.upload('kitten.png')
"http://avatars.io/4fb6de143d242d44da000001/hashashash"

# With a file object:
>>> fobj = open('kitten.png', 'rb')
>>> avtio.upload(fobj)
"http://avatars.io/4fb6de143d242d44da000001/hashashash"

# You can give a custom identifer:
>>> avtio.upload('kitten.png', 'my-identifier')
"http://avatars.io/4fb6de143d242d44da000001/my-identifier"

# And obviously, build sersvice avatar URLs:
# (but sersiouly, you don't need the lib for that)
>>> AvatarsIO.avatar_url('twitter', 'my-identifier')
"http://avatars.io/twitter/my-identifier"
```

Licence
-------
MIT

Extra stuff
-----------
Feel free to submit bug reports and improvements on the
[bug tracker](https://github.com/Zopieux/avatars-io-python/issues).
