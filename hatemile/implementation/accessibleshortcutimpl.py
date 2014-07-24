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

from hatemile import AccessibleShortcut
import re

class AccessibleShortcutImpl(AccessibleShortcut):
	"""
	The AccessibleShortcutImpl class is official implementation of
	AccessibleShortcut interface.
	__version__ = 2014-07-23
	"""
	
	def __init__(self, parser, configure, userAgent = None):
		"""
		Initializes a new object that manipulate the accessibility of the
		shortcuts of parser.
		@param parser: The HTML parser.
		@type parser: L{hatemile.util.HTMLDOMParser}
		@param configure: The configuration of HaTeMiLe.
		@type configure: L{hatemile.util.Configure}
		@param userAgent: The user agent of the user.
		@type userAgent: str
		"""
		
		self.parser = parser
		self.idContainerShortcuts = configure.getParameter('id-container-shortcuts')
		self.idSkipLinkContainerShortcuts = configure.getParameter('id-skip-link-container-shortcuts')
		self.idSkipContainerShortcuts = configure.getParameter('id-skip-container-shortcuts')
		self.idTextShortcuts = configure.getParameter('id-text-shortcuts')
		self.textSkipLinkContainerShortcuts = configure.getParameter('text-skip-container-shortcuts')
		self.textShortcuts = configure.getParameter('text-shortcuts')
		self.standartPrefix = configure.getParameter('text-standart-shortcut-prefix')
		self.dataAccessKey = 'data-' + configure.getParameter('data-accesskey')
		self.dataIgnore = 'data-' + configure.getParameter('data-ignore')
		self.listAdded = False
		self.list = None
		
		if userAgent != None:
			userAgent = userAgent.downcase()
			opera = 'opera' in userAgent
			mac = 'mac' in userAgent
			konqueror = 'konqueror' in userAgent
			spoofer = 'spoofer' in userAgent
			safari = 'applewebkit' in userAgent
			windows = 'windows' in userAgent
			chrome = 'chrome' in userAgent
			firefox = re.match('.*firefox/[2-9]|minefield/3.*', userAgent) != None
			ie = ('msie' in userAgent) or ('trident' in userAgent) 
			
			if opera:
				self.prefix = 'SHIFT + ESC'
			elif chrome and mac and (not spoofer):
				self.prefix = 'CTRL + OPTION'
			elif safari and (not windows) and (not spoofer):
				self.prefix = 'CTRL + ALT'
			elif (not windows) and (safari or mac or konqueror):
				self.prefix = 'CTRL'
			elif firefox:
				self.prefix = 'ALT + SHIFT'
			elif chrome or ie:
				self.prefix = 'ALT'
			else:
				self.prefix = self.standartPrefix
		else:
			self.prefix = self.standartPrefix
	
	def _getDescription(self, element):
		"""
		Returns the description of element.
		@param element: The element with description.
		@type element: L{hatemile.util.HTMLDOMElement}
		@return: The description of element.
		@rtype: str
		"""
		
		description = None
		if element.hasAttribute('title'):
			description = element.getAttribute('title')
		elif element.hasAttribute('aria-label'):
			description = element.getAttribute('aria-label')
		elif element.hasAttribute('alt'):
			description = element.getAttribute('alt')
		elif element.hasAttribute('label'):
			description = element.getAttribute('label')
		elif (element.hasAttribute('aria-labelledby')) or (element.hasAttribute('aria-describedby')):
			if element.hasAttribute('aria-labelledby'):
				descriptionIds = re.split('[ \n\r\t]+', element.getAttribute('aria-labelledby').strip())
			else:
				descriptionIds = re.split('[ \n\r\t]+', element.getAttribute('aria-describedby').strip())
			for descriptionId in descriptionIds:
				elementDescription = self.parser.find('#' + descriptionId).firstResult()
				if elementDescription != None:
					description = elementDescription.getTextContent()
					break
		elif element.getTagName() == 'INPUT':
			typeAttribute = element.getAttribute('type').lower()
			if ((typeAttribute == 'button') or (typeAttribute == 'submit') or (typeAttribute == 'reset')) and (element.hasAttribute('value')):
				description = element.getAttribute('value')
		if not bool(description):
			description = element.getTextContent()
		return re.sub('[ \n\r\t]+', ' ', description.strip())
	
	def _generateList(self):
		"""
		Generate the list of shortcuts of page.
		@return: The list of shortcuts of page.
		@rtype: hatemile.util.HTMLDOMElement
		"""
		
		local = self.parser.find('body').firstResult()
		htmlList = None
		if local != None:
			container = self.parser.find('#' + self.idContainerShortcuts).firstResult()
			if container == None:
				container = self.parser.createElement('div')
				container.setAttribute('id', self.idContainerShortcuts)
				firstChild = local.getFirstElementChild()
				firstChild.insertBefore(container)
				
				anchorJump = self.parser.createElement('a')
				anchorJump.setAttribute('id', self.idSkipLinkContainerShortcuts)
				anchorJump.setAttribute('href', '#' + self.idSkipContainerShortcuts)
				anchorJump.appendText(self.textSkipLinkContainerShortcuts)
				container.insertBefore(anchorJump)
				
				anchor = self.parser.createElement('a')
				anchor.setAttribute('name', self.idSkipContainerShortcuts)
				anchor.setAttribute('id', self.idSkipContainerShortcuts)
				firstChild.insertBefore(anchor)
				
				textContainer = self.parser.createElement('span')
				textContainer.setAttribute('id', self.idTextShortcuts)
				textContainer.appendText(self.textShortcuts)
				container.appendElement(textContainer)
			htmlList = self.parser.find(container).findChildren('ul').firstResult()
			if htmlList == None:
				htmlList = self.parser.createElement('ul')
				container.appendElement(htmlList)
		self.listAdded = True
		
		return htmlList
	
	def getPrefix(self):
		return self.prefix
	
	def fixShortcut(self, element):
		if element.hasAttribute('accesskey'):
			description = self._getDescription(element)
			if not element.hasAttribute('title'):
				element.setAttribute('title', description)
			
			if not self.listAdded:
				self.list = self._generateList()
			
			if self.list != None:
				keys = re.split('[ \n\t\r]+', element.getAttribute('accesskey'))
				for key in keys:
					key = key.upper()
					if self.parser.find(self.list).findChildren('[' + self.dataAccessKey + '=' + key + ']').firstResult() == None:
						item = self.parser.createElement('li')
						item.setAttribute(self.dataAccessKey, key)
						item.appendText(self.prefix + ' + ' + key + ': ' + description)
						self.list.appendElement(item)
	
	def fixShortcuts(self):
		elements = self.parser.find('[accesskey]').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixShortcut(element)