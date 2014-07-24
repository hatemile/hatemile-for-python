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
	"""
	The AccessibleFormImpl class is official implementation of AccessibleForm
	interface.
	__version__ = 2014-07-23
	"""
	
	def __init__(self, parser, configure):
		"""
		Initializes a new object that manipulate the accessibility of the forms
		of parser.
		@param parser: The HTML parser.
		@type parser: L{hatemile.util.HTMLDOMParser}
		@param configure: The configuration of HaTeMiLe.
		@type configure: L{hatemile.util.Configure}
		"""
		
		self.parser = parser
		self.prefixId = configure.getParameter('prefix-generated-ids')
		self.dataLabelRequiredField = 'data-' + configure.getParameter('data-label-required-field')
		self.dataIgnore = 'data-' + configure.getParameter('data-ignore')
		self.prefixRequiredField = configure.getParameter('prefix-required-field')
		self.suffixRequiredField = configure.getParameter('suffix-required-field')
	
	def _fixLabelRequiredField(self, label, requiredField):
		"""
		Do the label or the aria-label to inform in label that the field is
		required.
		@param label: The label.
		@type label: L{hatemile.util.HTMLDOMElement}
		@param requiredField: The required field.
		@type requiredField: L{hatemile.util.HTMLDOMElement}
		"""
		
		if (requiredField.hasAttribute('required')) or ((requiredField.hasAttribute('aria-required')) and (requiredField.getAttribute('aria-required').lower() == 'true')):
			if not label.hasAttribute(self.dataLabelRequiredField):
				label.setAttribute(self.dataLabelRequiredField, 'true')
			
			if requiredField.hasAttribute('aria-label'):
				contentLabel = requiredField.getAttribute('aria-label')
				if (self.prefixRequiredField != '') and (self.prefixRequiredField not in contentLabel):
					contentLabel = self.prefixRequiredField + ' ' + contentLabel
				if (self.suffixRequiredField != '') and (self.suffixRequiredField not in contentLabel):
					contentLabel = contentLabel + ' ' + self.suffixRequiredField
				requiredField.setAttribute('aria-label', contentLabel)
	
	def _fixControlAutoComplete(self, control, active):
		"""
		Fix the control to inform if it has autocomplete and the type.
		@param control: The form control.
		@type control: L{hatemile.util.HTMLDOMElement}
		@param active: If the element has autocomplete.
		@type active: bool
		"""
		
		if active == True:
			control.setAttribute('aria-autocomplete', 'both')
		elif not ((active == None) and (control.hasAttribute('aria-autocomplete'))):
			if control.hasAttribute('list'):
				datalist = self.parser.find('datalist[id=' + control.getAttribute('list') + ']').firstResult()
				if datalist != None:
					control.setAttribute('aria-autocomplete', 'list')
			if (active == False) and ((not control.hasAttribute('aria-autocomplete')) or (control.getAttribute('aria-autocomplete').lower() != 'list')):
				control.setAttribute('aria-autocomplete', 'none')
	
	def fixRequiredField(self, requiredField):
		if requiredField.hasAttribute('required'):
			requiredField.setAttribute('aria-required', 'true')
			
			labels = None
			if requiredField.hasAttribute('id'):
				labels = self.parser.find('label[for=' + requiredField.getAttribute('id') + ']').listResults()
			if not bool(labels):
				labels = self.parser.find(requiredField).findAncestors('label').listResults()
			for label in labels:
				self._fixLabelRequiredField(label, requiredField)
	
	def fixRequiredFields(self):
		requiredFields = self.parser.find('[required]').listResults()
		for requiredField in requiredFields:
			if not requiredField.hasAttribute(self.dataIgnore):
				self.fixRequiredField(requiredField)
	
	def fixRangeField(self, rangeField):
		if rangeField.hasAttribute('min'):
			rangeField.setAttribute('aria-valuemin', rangeField.getAttribute('min'))
		if rangeField.hasAttribute('max'):
			rangeField.setAttribute('aria-valuemax', rangeField.getAttribute('max'))
	
	def fixRangeFields(self):
		rangeFields = self.parser.find('[min],[max]').listResults()
		for rangeField in rangeFields:
			if not rangeField.hasAttribute(self.dataIgnore):
				self.fixRangeField(rangeField)
	
	def fixLabel(self, label):
		if label.getTagName() == 'LABEL':
			field = None
			if label.hasAttribute('for'):
				field = self.parser.find('#' + label.getAttribute('for')).firstResult()
			else:
				field = self.parser.find(label).findDescendants('input,select,textarea').firstResult()
				
				if field != None:
					CommonFunctions.generateId(field, self.prefixId)
					label.setAttribute('for', field.getAttribute('id'))
			if field != None:
				if not field.hasAttribute('aria-label'):
					field.setAttribute('aria-label', re.sub('[ \n\r\t]+', ' ', label.getTextContent().strip()))
				
				self._fixLabelRequiredField(label, field)
				
				CommonFunctions.generateId(label, self.prefixId)
				field.setAttribute('aria-labelledby', CommonFunctions.increaseInList(field.getAttribute('aria-labelledby'), label.getAttribute('id')))
	
	def fixLabels(self):
		labels = self.parser.find('label').listResults()
		for label in labels:
			if not label.hasAttribute(self.dataIgnore):
				self.fixLabel(label)
	
	def fixAutoComplete(self, element):
		if element.hasAttribute('autocomplete'):
			active = None
			value = element.getAttribute('autocomplete')
			if value == 'on':
				active = True
			elif value == 'off':
				active = False
			if active != None:
				if element.getTagName() == 'FORM':
					controls = self.parser.find(element).findDescendants('input,textarea').listResults()
					if element.hasAttribute('id'):
						idElement = element.getAttribute('id')
						controls = controls + self.parser.find('input[form=' + idElement + '],textarea[form=' + idElement + ']').listResults()
					for control in controls:
						fix = True
						if (control.getTagName() == 'INPUT') and (control.hasAttribute('type')):
							typeControl = control.getAttribute('type').lower()
							if (typeControl == 'button') or (typeControl == 'submit') or (typeControl == 'reset') or (typeControl == 'image') or (typeControl == 'file') or (typeControl == 'checkbox') or (typeControl == 'radio') or (typeControl == 'password') or (typeControl == 'hidden'):
								fix = False
						if fix:
							autoCompleteControlFormValue = control.getAttribute('autocomplete')
							if 'on' == autoCompleteControlFormValue:
								self._fixControlAutoComplete(control, True)
							elif 'off' == autoCompleteControlFormValue:
								self._fixControlAutoComplete(control, False)
							else:
								self._fixControlAutoComplete(control, active)
				else:
					self._fixControlAutoComplete(element, active)
		if (not element.hasAttribute('aria-autocomplete')) and (element.hasAttribute('list')):
			self._fixControlAutoComplete(element, None)
	
	def fixAutoCompletes(self):
		elements = self.parser.find('[autocomplete],[list]').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixAutoComplete(element)