#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

import json

from google.appengine.api import memcache

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')
        memcache.set('data', "[]")

class WriteHandler(webapp2.RequestHandler):
	def get(self):
		memcache.set('data', self.request.get('data'))

class GetHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write(memcache.get('data'))

class WriteToBufferHandler(webapp2.RequestHandler):
	def get(self):
		data = self.request.get('data')
		if memcache.get('data') is None:
			memcache.set('data', "[]")
		p = json.loads(memcache.get('data'))
		p.append(data)
		memcache.set('data', json.dumps(p))

class GetFromBufferHandler(webapp2.RequestHandler):
	def get(self):
		if memcache.get('data') is None:
			memcache.set('data', "[]")
		p = json.loads(memcache.get('data'))
		result = ""
		if p:
			result = p[0]
			if len(p) > 1:
				p = p[1:]
			else:
				p = []
		memcache.set('data', json.dumps(p))
		self.response.write(result)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/write_old', WriteHandler),
    ('/write', WriteToBufferHandler),
    ('/get', GetFromBufferHandler),
    ('/get_old', GetHandler),
], debug=True)
