#Copyright 2014 Carlson Santana Cruz
#
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

from xml.dom import minidom
from selectorchange import SelectorChange

class Configure:
	"""
	The Configure class contains the configuration of HaTeMiLe.
	__version__ = 2014-07-23
	"""
	
	def __init__(self, fileName = None):
		"""
		Initializes a new object that contains the configuration of HaTeMiLe.
		@param fileName: The full path of file.
		@type fileName: str
		"""
		
		self.parameters = {}
		self.selectorChanges = []
		if fileName == None:
			fileName = 'hatemile-configure.xml'
		xmldoc = minidom.parse(fileName)
		params = xmldoc.getElementsByTagName('parameters')[0].getElementsByTagName('parameter')
		for param in params:
			if param.hasChildNodes():
				self.parameters[param.attributes['name'].value] = param.firstChild.nodeValue
			else:
				self.parameters[param.attributes['name'].value] = ''
		changes = xmldoc.getElementsByTagName('selector-changes')[0].getElementsByTagName('selector-change')
		for change in changes:
			self.selectorChanges.append(SelectorChange(change.attributes['selector'].value, change.attributes['attribute'].value, change.attributes['value-attribute'].value))
	
	def getParameters(self):
		"""
		Returns the parameters of configuration.
		@return: The parameters of configuration.
		@rtype: dict
		"""
		
		return self.parameters.copy()
	
	def getParameter(self, name):
		"""
		Returns the value of a parameter of configuration.
		@param name: The parameter.
		@type name: str
		@return: The value of the parameter.
		@rtype: str
		"""
		
		return self.parameters[name]
	
	def getSelectorChanges(self):
		"""
		Returns the changes that will be done in selectors.
		@return: The changes that will be done in selectors.
		@rtype: array.L{hatemile.util.SelectorChange}
		"""
		
		return [] + self.selectorChanges