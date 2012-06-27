# coding: utf-8

# Python 2; doesn't fail in Python 3
from __future__ import unicode_literals

import os
import json
import requests
from hashlib import md5

class AvatarsIOException(Exception): pass

def block_md5(fileobj, block_size=2**15):
	hashed = md5()
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
		print response.content
		raise AvatarsIOException("Malformed response from avatars.io")

class AvatarsIO(object):
	"""
		Usage:
		>>> avtio = AvatarsIO('my-client-id', 'my-access-token')

		With a file name:
		>>> upload_id = avtio.upload(fname)
		"http://avatars.io/4fb6de143d242d44da000001/hashashash"

		With a file object:
		>>> fobj = open(fname, 'rb')
		>>> upload_id = avtio.upload(fobj)
		"http://avatars.io/4fb6de143d242d44da000001/hashashash"

		You can give a custom identifer:
		>>> upload_id = avtio.upload(fname, 'my-identifier')
		"http://avatars.io/4fb6de143d242d44da000001/my-identifier"

		Build custom avatar URL:
		>>> url = AvatarsIO.avatar_url('twitter', 'my-identifier')
		"http://avatars.io/twitter/my-identifier"
	"""
	base_uri = 'http://avatars.io'

	def __init__(self, client_id, access_token):
		self.client_id = client_id
		self.access_token = access_token

	def upload(self, file, identifer=''):
		"""
			Uploads a file to Avarats.IO.
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
			data=json.dumps({
				'filename': file_name,
				'md5': block_md5(file),
				'size': file_size,
				'path': identifer,
			})
		)
		print response.request.headers

		data = response_to_json(response)
		print data
		if not 'upload_info' in data['data']:
			return data['data']['url']

		infos = data['data']['upload_info']

		file.seek(0)
		requests.put(infos['upload_url'],
			headers={
				'authorization': infos.get('signature'),
				'date': infos.get('date'),
				'content-type': infos.get('content-type'),
				'x-amz-acl': 'public-read',
			},
			files={'upload': file}
		)

		response = requests.post(AvatarsIO.base_uri + 'v1/token/%s/complete' % data['id'],
			headers={
				'x-client_id': self.client_id,
				'authorization': 'OAuth %s' % self.access_token,
			})
		return response_to_json(response)['data']

	@staticmethod
	def avatar_url(service, identifer):
		return '%s/%s/%s' % (AvatarsIO.base_uri, service, identifer)
