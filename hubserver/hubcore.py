"""
The MIT License (MIT)

Copyright (c) 2015 Gareth Nelson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import hashlib
import hmac
from enum import Enum
import sets

class FeedType(Enum):
   EVENT = 1
   BIN   = 2
   INPUT = 3

class CyborgNetFeed:
   def __init__(self,feed_id='',feed_type=FeedType.EVENT,is_public=False,publisher=None):
       self.feed_id     = feed_id
       self.feed_type   = feed_type
       self.is_public   = is_public
       self.subscribers = sets.Set()
       self.publisher   = publisher

class HubServerCore:
   def __init__(self):
       self.connections           = []
       self.feeds                 = {}
       self.paired_module_secrets = {}
   def pair_module(self,module_id,shared_secret):
       """ Adds the module as a paired module or updates the shared secret
       """
       self.paired_module_secrets[module_id] = shared_secret
   def is_paired(self,module_id):
       """ Responds with boolean indicating whether or not the module is paired
       """
       return self.paired_module_secrets.has_key(module_id)
   def auth_module(self,module_id,challenge,response):
       """ Checks if the response to the challenge string is correct
       """
       secret       = self.paired_module_secrets[module_id]
       correct_resp = hmac.new(secret,challenge,hashlib.sha256).hexdigest()
       if response == correct_resp: return True
       return False

