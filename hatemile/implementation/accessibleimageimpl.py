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

from hatemile.util import CommonFunctions
from hatemile import AccessibleImage

class AccessibleImageImpl(AccessibleImage):
	"""
	The AccessibleImageImpl class is official implementation of AccessibleImage
	interface.
	__version__ = 2014-07-23
	"""
	
	def __init__(self, parser, configure):
		"""
		Initializes a new object that manipulate the accessibility of the images
		of parser.
		@param parser: The HTML parser.
		@type parser: L{hatemile.util.HTMLDOMParser}
		@param configure: The configuration of HaTeMiLe.
		@type configure: L{hatemile.util.Configure}
		"""
		
		self.parser = parser
		self.prefixId = configure.getParameter('prefix-generated-ids')
		self.classListImageAreas = configure.getParameter('class-list-image-areas')
		self.classLongDescriptionLink = configure.getParameter('class-longdescription-link')
		self.prefixLongDescriptionLink = configure.getParameter('prefix-longdescription-link')
		self.suffixLongDescriptionLink = configure.getParameter('suffix-longdescription-link')
		self.dataListForImage = 'data-' + configure.getParameter('data-list-for-image')
		self.dataLongDescriptionForImage = 'data-' + configure.getParameter('data-longdescription-for-image')
		self.dataIgnore = 'data-' + configure.getParameter('data-ignore')
	
	def fixMap(self, elementMap):
		if elementMap.getTagName() == 'MAP':
			name = None
			if elementMap.hasAttribute('name'):
				name = elementMap.getAttribute('name')
			elif elementMap.hasAttribute('id'):
				name = elementMap.getAttribute('id')
			if bool(name):
				elementList = self.parser.createElement('ul')
				areas = self.parser.find(elementMap).findChildren('area[alt]').listResults()
				for area in areas:
					item = self.parser.createElement('li')
					anchor = self.parser.createElement('a')
					anchor.appendText(area.getAttribute('alt'))
					
					CommonFunctions.setListAttributes(area, anchor, ['href', 'tabindex'
							, 'target', 'download', 'hreflang', 'media', 'nohref', 'ping', 'rel'
							, 'type', 'title', 'accesskey', 'name', 'onblur', 'onfocus', 'onmouseout'
							, 'onmouseover', 'onkeydown', 'onkeypress', 'onkeyup', 'onmousedown'
							, 'onclick', 'ondblclick', 'onmouseup'])
					
					item.appendElement(anchor)
					elementList.appendElement(item)
				if elementList.hasChildren():
					elementList.setAttribute('class', self.classListImageAreas)
					images = self.parser.find('[usemap=#' + name + ']').listResults()
					for image in images:
						CommonFunctions.generateId(image, self.prefixId)
						idElement = image.getAttribute('id')
						if self.parser.find('[' + self.dataListForImage + '=' + idElement + ']').firstResult() == None:
							newList = elementList.cloneElement()
							newList.setAttribute(self.dataListForImage, idElement)
							image.insertAfter(newList)
	
	def fixMaps(self):
		maps = self.parser.find('map').listResults()
		for elementMap in maps:
			if not elementMap.hasAttribute(self.dataIgnore):
				self.fixMap(elementMap)
	
	def fixLongDescription(self, element):
		if element.hasAttribute('longdesc'):
			CommonFunctions.generateId(element, self.prefixId)
			idElement = element.getAttribute('id')
			if self.parser.find('[' + self.dataLongDescriptionForImage + '=' + idElement + ']').firstResult() == None:
				if element.hasAttribute('alt'):
					text = self.prefixLongDescriptionLink + ' ' + element.getAttribute('alt') + ' ' + self.suffixLongDescriptionLink
				else:
					text = self.prefixLongDescriptionLink + ' ' + self.suffixLongDescriptionLink
				anchor = self.parser.createElement('a')
				anchor.setAttribute('href', element.getAttribute('longdesc'))
				anchor.setAttribute('target', '_blank')
				anchor.setAttribute(self.dataLongDescriptionForImage, idElement)
				anchor.setAttribute('class', self.classLongDescriptionLink)
				anchor.appendText(text.strip())
				element.insertAfter(anchor)
	
	def fixLongDescriptions(self):
		elements = self.parser.find('[longdesc]').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixLongDescription(element)