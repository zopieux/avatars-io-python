#!/usr/bin/env python
# coding: utf-8

# Copyright 2008-2012 Alexandre `Zopieux` Macabies
# This module is part of avatarsio and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import os
import json
import requests
import hashlib

class AvatarsIOException(Exception): pass

def block_md5(fileobj, block_size=2**18):
	hashed = hashlib.md5()
	while True:
		data = fileobj.read(block_size)
		if not data:
			break
		hashed.update(data)
	return hashed.hexdigest()

def response_to_json(response, encoding='utf-8'):
	try:
		return json.loads(response.content.decode('utf-8'))
	except ValueError:
		raise AvatarsIOException("Malformed response from avatars.io")

class AvatarsIO(object):
	"""
		Usage:
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
	"""
	base_uri = 'http://avatars.io'

	def __init__(self, client_id, access_token):
		"""
			You need a Chute app to get your client_id (called "App ID")
			and access_token.
			See http://apps.getchute.com/apps/new
		"""
		self.client_id = client_id
		self.access_token = access_token

	def upload(self, file, identifer=''):
		"""
			Uploads a file to Avatars.io.
			`file` can be either a file path or a file object with a `read`
			attribute.
		"""
		try:
			should_open = isinstance(file, basestring)
		except NameError: # Python 3
			should_open = isinstance(file, str)
		if should_open:
			file_name = file
			file_size = os.path.getsize(file)
			file = open(file, 'rb')
		else:
			file.seek(0, os.SEEK_END)
			file_size = file.tell()
			try:
				file_name = file.name
			except AttributeError:
				file_name = 'unknow-filename'

		file.seek(0)
		response = requests.post(AvatarsIO.base_uri + '/v1/token',
			headers={
				'x-client_id': self.client_id,
				'authorization': 'OAuth %s' % self.access_token
			},
			data={
				'data[filename]': file_name,
				'data[md5]': block_md5(file),
				'data[size]': file_size,
				'data[path]': identifer
			}
		)

		data = response_to_json(response)

		if not 'upload_info' in data['data']:
			return data['data']['url']

		id = data['data']['id']
		infos = data['data']['upload_info']

		file.seek(0)
		requests.put(infos['upload_url'],
			headers={
				'authorization': infos.get('signature'),
				'date': infos.get('date'),
				'content-type': infos.get('content_type'),
				'x-amz-acl': 'public-read',
			},
			data=file
		)

		response = requests.post(AvatarsIO.base_uri + '/v1/token/%s/complete' % id,
			headers={
				'x-client_id': self.client_id,
				'authorization': 'OAuth %s' % self.access_token,
			}
		)
		return response_to_json(response)['data']

	@staticmethod
	def avatar_url(service, identifer):
		return '%s/%s/%s' % (AvatarsIO.base_uri, service, identifer)
