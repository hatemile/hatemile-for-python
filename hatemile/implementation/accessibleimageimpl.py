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
	def __init__(self, parser, configure):
		self.parser = parser
		self.prefixId = configure.getParameter('prefix-generated-ids')
		self.classListImageAreas = configure.getParameter('class-list-image-areas')
		self.classLongDescriptionLink = configure.getParameter('class-longdescription-link')
		self.textLongDescriptionLink = configure.getParameter('text-longdescription-link')
		self.dataListForImage = configure.getParameter('data-list-for-image')
		self.dataLongDescriptionForImage = configure.getParameter('data-longdescription-for-image')
		self.dataIgnore = configure.getParameter('data-ignore')
	def fixMap(self, element):
		if element.getTagName() == 'MAP':
			name = None
			if element.hasAttribute('name'):
				name = element.getAttribute('name')
			elif element.hasAttribute('id'):
				name = element.getAttribute('id')
			if bool(name):
				listTag = self.parser.createElement('ul')
				listTag.setAttribute('class', self.classListImageAreas)
				areas = self.parser.find(element).findChildren('area, a').listResults()
				for area in areas:
					if area.hasAttribute('alt'):
						item = self.parser.createElement('li')
						anchor = self.parser.createElement('a')
						anchor.appendText(area.getAttribute('alt'))
						CommonFunctions.setListAttributes(area, anchor, ['href',
								'target', 'download', 'hreflang', 'media',
								'rel', 'type', 'title'])
						item.appendElement(anchor)
						listTag.appendElement(item)
				if listTag.hasChildren():
					images = self.parser.find('[usemap=#' + name + ']').listResults()
					for image in images:
						CommonFunctions.generateId(image, self.prefixId)
						if self.parser.find('[' + self.dataListForImage + '=' + image.getAttribute('id') + ']').firstResult() == None:
							newList = listTag.cloneElement()
							newList.setAttribute(self.dataListForImage, image.getAttribute('id'))
							image.insertAfter(newList)
	def fixMaps(self):
		elements = self.parser.find('map').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixMap(element)
	def fixLongDescription(self, element):
		if element.hasAttribute('longdesc'):
			CommonFunctions.generateId(element, self.prefixId)
			if self.parser.find('[' + self.dataLongDescriptionForImage + '=' + element.getAttribute('id') + ']').firstResult() == None:
				text = None
				if element.hasAttribute('alt'):
					text = element.getAttribute('alt') + ' ' + self.textLongDescriptionLink
				else:
					text = self.textLongDescriptionLink
				longDescription = element.getAttribute('longdesc')
				anchor = self.parser.createElement('a')
				anchor.setAttribute('href', longDescription)
				anchor.setAttribute('target', '_blank')
				anchor.setAttribute(self.dataLongDescriptionForImage, element.getAttribute('id'))
				anchor.setAttribute('class', self.classLongDescriptionLink)
				anchor.appendText(text)
				element.insertAfter(anchor)
	def fixLongDescriptions(self):
		elements = self.parser.find('[longdesc]').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixLongDescription(element)