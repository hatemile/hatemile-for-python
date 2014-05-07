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
from hatemile import AccessibleForm
import re

class AccessibleFormImpl(AccessibleForm):
	def __init__(self, parser, configure):
		self.parser = parser
		self.prefixId = configure.getParameter('prefix-generated-ids')
		self.classRequiredField = configure.getParameter('class-required-field')
		self.sufixRequiredField = configure.getParameter('sufix-required-field')
		self.dataIgnore = configure.getParameter('data-ignore')
	def fixRequiredField(self, element):
		if element.hasAttribute('required'):
			element.setAttribute('aria-required', 'true')
			labels = None
			if element.hasAttribute('id'):
				labels = self.parser.find('label[for=' + element.getAttribute('id') + ']').listResults()
			if not bool(labels):
				labels = self.parser.find(element).findAncestors('label').listResults()
			for label in labels:
				label.setAttribute('class', CommonFunctions.increaseInList(label.getAttribute('class'), self.classRequiredField))
	def fixRequiredFields(self):
		elements = self.parser.find('[required]').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixRequiredField(element)
	def fixDisabledField(self, element):
		if element.hasAttribute('disabled'):
			element.setAttribute('aria-disabled', 'true')
	def fixDisabledFields(self):
		elements = self.parser.find('[disabled]').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixDisabledField(element)
	def fixReadOnlyField(self, element):
		if element.hasAttribute('readonly'):
			element.setAttribute('aria-readonly', 'true')
	def fixReadOnlyFields(self):
		elements = self.parser.find('[readonly]').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixReadOnlyField(element)
	def fixRangeField(self, element):
		if element.hasAttribute('min'):
			element.setAttribute('aria-valuemin', element.getAttribute('min'))
		if element.hasAttribute('max'):
			element.setAttribute('aria-valuemax', element.getAttribute('max'))
	def fixRangeFields(self):
		elements = self.parser.find('[min],[max]').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixRangeField(element)
	def fixTextField(self, element):
		if (element.getTagName() == 'INPUT') and (element.hasAttribute('type')):
			typeAttribute = element.getAttribute('type').lower()
			if (typeAttribute == 'text') or (typeAttribute == 'search') or (typeAttribute == 'email') or (typeAttribute == 'url') or (typeAttribute == 'tel') or (typeAttribute == 'number'):
				element.setAttribute('aria-multiline', 'false')
		elif element.getTagName() == 'TEXTAREA':
			element.setAttribute('aria-multiline', 'true')
	def fixTextFields(self):
		elements = self.parser.find('input[type=text],input[type=search],input[type=email],input[type=url],input[type=tel],input[type=number],textarea').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixTextField(element)
	def fixSelectField(self, element):
		if element.getTagName() == 'SELECT':
			if element.hasAttribute('multiple'):
				element.setAttribute('aria-multiselectable', 'true')
			else:
				element.setAttribute('aria-multiselectable', 'false')
	def fixSelectFields(self):
		elements = self.parser.find('select').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixSelectField(element)
	def fixLabel(self, element):
		if element.getTagName() == 'LABEL':
			inputTag = None
			if element.hasAttribute('for'):
				inputTag = self.parser.find('#' + element.getAttribute('for')).firstResult()
			else:
				inputTag = self.parser.find(element).findDescendants('input,select,textarea').firstResult()
				if inputTag != None:
					CommonFunctions.generateId(inputTag, self.prefixId)
					element.setAttribute('for', inputTag.getAttribute('id'))
			if inputTag != None:
				if not inputTag.hasAttribute('aria-label'):
					label = re.sub('[ \n\r\t]+', ' ', element.getTextContent().strip())
					if inputTag.hasAttribute('aria-required'):
						if (inputTag.getAttribute('aria-required').lower() == 'true') and (not self.sufixRequiredField in label):
							label += ' ' + self.sufixRequiredField
					inputTag.setAttribute('aria-label', label)
				CommonFunctions.generateId(element, self.prefixId)
				inputTag.setAttribute('aria-labelledby', CommonFunctions.increaseInList(inputTag.getAttribute('aria-labelledby'), element.getAttribute('id')))
	def fixLabels(self):
		elements = self.parser.find('label').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixLabel(element)