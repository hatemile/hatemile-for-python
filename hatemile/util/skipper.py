#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import re

class Skipper:
	"""
	The Skipper class store the selector that will be add a skipper.
	"""
	
	def __init__(self, selector = None, defaultText = None, shortcuts = None):
		"""
		Inicializes a new object with the values pre-defineds.
		@param selector: The selector.
		@type selector: str
		@param defaultText: The default text of skipper.
		@type defaultText: str
		@param shortcuts: The shortcuts of skipper.
		@type shortcuts: str
		"""
		
		self.selector = selector
		self.defaultText = defaultText
		if shortcuts == '':
			self.shortcuts = []
		else:
			self.shortcuts = re.split('[ \n\t\r]+', shortcuts)
	
	def getSelector(self):
		"""
		Returns the selector.
		@return: The selector.
		@rtype: str
		"""
		
		return self.selector
	
	def getDefaultText(self):
		"""
		Returns the default text of skipper.
		@return: The default text of skipper.
		@rtype: str
		"""
		
		return self.defaultText
	
	def getShortcuts(self):
		"""
		Returns the shortcuts of skipper.
		@return: The shortcuts of skipper.
		@rtype: str
		"""
		
		return [] + self.shortcuts