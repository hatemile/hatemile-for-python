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
	def __init__(self, parser, configure, userAgent = None):
		self.parser = parser
		self.idContainerShortcuts = configure.getParameter('id-container-shortcuts')
		self.idSkipLinkContainerShortcuts = configure.getParameter('id-skip-link-container-shortcuts')
		self.idSkipContainerShortcuts = configure.getParameter('id-skip-container-shortcuts')
		self.dataAccessKey = configure.getParameter('data-accesskey')
		self.textSkipLinkContainerShortcuts = configure.getParameter('text-skip-container-shortcuts')
		self.dataIgnore = configure.getParameter('data-ignore')
		self.list = None
		if userAgent != None:
			userAgent = userAgent.downcase()
			mac = 'mac' in userAgent
			konqueror = 'konqueror' in userAgent
			spoofer = 'spoofer' in userAgent
			safari = 'applewebkit' in userAgent
			windows = 'windows' in userAgent
			if 'opera' in userAgent:
				self.prefix = 'SHIFT + ESC'
			elif 'chrome' in userAgent and (not spoofer) and mac:
				self.prefix = 'CTRL + OPTION'
			elif safari and (not windows) and (not spoofer):
				self.prefix = 'CTRL + ALT'
			elif (not windows) and (safari or mac or konqueror):
				self.prefix = 'CTRL'
			elif re.match('.*firefox/[2-9]|minefield/3.*', userAgent) != None:
				self.prefix = 'ALT + SHIFT'
			else:
				self.prefix = 'ALT'
		else:
			self.prefix = 'ALT'
	def getDescription(self, element):
		description = ''
		if element.hasAttribute('title'):
			description = element.getAttribute('title')
		elif element.hasAttribute('aria-labelledby'):
			labelsIds = re.split('[ \n\r\t]+', element.getAttribute('aria-labelledby').strip())
			for labelId in labelsIds:
				label = self.parser.find('#' + labelId).firstResult()
				if label != None:
					description = label.getTextContent()
					break
		elif element.hasAttribute('aria-label'):
			description = element.getAttribute('aria-label')
		elif element.hasAttribute('alt'):
			description = element.getAttribute('alt')
		elif element.getTagName() == 'INPUT':
			typeAttribute = element.getAttribute('type').lower()
			if ((typeAttribute == 'button') or (typeAttribute == 'submit') or (typeAttribute == 'reset')) and element.hasAttribute('value'):
				description = element.getAttribute('value')
		else:
			description = element.getTextContent()
		return re.sub('[ \n\r\t]+', ' ', description.strip())
	def generateList(self):
		container = self.parser.find('#' + self.idContainerShortcuts).firstResult()
		if container == None:
			container = self.parser.createElement('div')
			container.setAttribute('id', self.idContainerShortcuts)
			firstChild = self.parser.find('body').firstResult().getFirstElementChild()
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
		htmlList = self.parser.find(container).findChildren('ul').firstResult()
		if htmlList == None:
			htmlList = self.parser.createElement('ul')
			container.appendElement(htmlList)
		return htmlList
	def getPrefix(self):
		return self.prefix
	def fixShortcut(self, element):
		if element.hasAttribute('accesskey'):
			description = self.getDescription(element)
			if not element.hasAttribute('title'):
				element.setAttribute('title', description)
			keys = re.split(' ', element.getAttribute('accesskey'))
			if self.list == None:
				self.list = self.generateList()
			for key in keys:
				key = key.upper()
				if self.parser.find(self.list).findChildren('[' + self.dataAccessKey + '=' + 'key' + ']').firstResult() == None:
					item = self.parser.createElement('li')
					item.setAttribute(self.dataAccessKey, key)
					item.appendText(self.prefix + ' + ' + key + ': ' + description)
					self.list.appendElement(item)
	def fixShortcuts(self):
		elements = self.parser.find('[accesskey]').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixShortcut(element)