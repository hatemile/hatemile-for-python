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

class AccessibleForm:
	"""
	The AccessibleForm interface fix the problems of accessibility associated
	with the forms.
	__version__ = 2014-07-23
	"""
	
	def fixRequiredField(self, requiredField):
		"""
		Fix required field.
		@param requiredField: The element that will be fixed.
		@type requiredField: L{hatemile.util.HTMLDOMElement}
		@see: U{H90: Indicating required form controls using label or legend<http://www.w3.org/TR/WCAG20-TECHS/H90.html>}
		@see: U{ARIA2: Identifying a required field with the aria-required property<http://www.w3.org/TR/2014/NOTE-WCAG20-TECHS-20140311/ARIA2>}
		@see: U{F81: Failure of Success Criterion 1.4.1 due to identifying required or error fields using color differences only<http://www.w3.org/TR/WCAG20-TECHS/F81.html>}
		@see: U{aria-required (property) | Supported States and Properties<http://www.w3.org/TR/wai-aria/states_and_properties#aria-required>}
		"""
		
		pass
	
	def fixRequiredFields(self):
		"""
		Fix required fields.
		@see: U{H90: Indicating required form controls using label or legend<http://www.w3.org/TR/WCAG20-TECHS/H90.html>}
		@see: U{ARIA2: Identifying a required field with the aria-required property<http://www.w3.org/TR/2014/NOTE-WCAG20-TECHS-20140311/ARIA2>}
		@see: U{F81: Failure of Success Criterion 1.4.1 due to identifying required or error fields using color differences only<http://www.w3.org/TR/WCAG20-TECHS/F81.html>}
		@see: U{aria-required (property) | Supported States and Properties<http://www.w3.org/TR/wai-aria/states_and_properties#aria-required>}
		"""
		
		pass
	
	def fixRangeField(self, rangeField):
		"""
		Fix range field.
		@param rangeField: The element that will be fixed.
		@type rangeField: L{hatemile.util.HTMLDOMElement}
		@see: U{aria-valuemin (property) | Supported States and Properties<http://www.w3.org/TR/wai-aria/states_and_properties#aria-valuemin>}
		@see: U{aria-valuemax (property) | Supported States and Properties<http://www.w3.org/TR/wai-aria/states_and_properties#aria-valuemax>}
		@see: U{Using WAI-ARIA range attributes for range widgets such as progressbar, scrollbar, slider and spinbutton<http://www.w3.org/WAI/GL/wiki/Using_WAI-ARIA_range_attributes_for_range_widgets_such_as_progressbar,_scrollbar,_slider,_and_spinbutton>}
		@see: U{ARIA3: Identifying valid range information with the aria-valuemin and aria-valuemax properties<http://www.w3.org/WAI/GL/2013/WD-WCAG20-TECHS-20130711/ARIA3.html>}
		"""
		
		pass
	
	def fixRangeFields(self):
		"""
		Fix range fields.
		@see: U{aria-valuemin (property) | Supported States and Properties<http://www.w3.org/TR/wai-aria/states_and_properties#aria-valuemin>}
		@see: U{aria-valuemax (property) | Supported States and Properties<http://www.w3.org/TR/wai-aria/states_and_properties#aria-valuemax>}
		@see: U{Using WAI-ARIA range attributes for range widgets such as progressbar, scrollbar, slider and spinbutton<http://www.w3.org/WAI/GL/wiki/Using_WAI-ARIA_range_attributes_for_range_widgets_such_as_progressbar,_scrollbar,_slider,_and_spinbutton>}
		@see: U{ARIA3: Identifying valid range information with the aria-valuemin and aria-valuemax properties<http://www.w3.org/WAI/GL/2013/WD-WCAG20-TECHS-20130711/ARIA3.html>}
		"""
		
		pass
	
	def fixLabel(self, label):
		"""
		Fix field associated with the label.
		@param label: The element that will be fixed.
		@type label: L{hatemile.util.HTMLDOMElement}
		@see: U{aria-label (property) | Supported States and Properties<http://www.w3.org/TR/wai-aria/states_and_properties#aria-label>}
		@see: U{aria-labelledby (property) | Supported States and Properties<http://www.w3.org/TR/wai-aria/states_and_properties#aria-labelledby>}
		"""
		
		pass
	
	def fixLabels(self):
		"""
		Fix fields associated with the labels.
		@see: U{aria-label (property) | Supported States and Properties<http://www.w3.org/TR/wai-aria/states_and_properties#aria-label>}
		@see: U{aria-labelledby (property) | Supported States and Properties<http://www.w3.org/TR/wai-aria/states_and_properties#aria-labelledby>}
		"""
		
		pass
	
	def fixAutoComplete(self, element):
		"""
		Fix element to inform if has autocomplete and the type.
		@param element: The element that will be fixed.
		@type element: L{hatemile.util.HTMLDOMElement}
		@see: U{aria-autocomplete (property) | Supported States and Properties<http://www.w3.org/TR/wai-aria/states_and_properties#aria-autocomplete>}
		"""
		
		pass
	
	def fixAutoCompletes(self):
		"""
		Fix elements to inform if has autocomplete and the type.
		@see: U{aria-autocomplete (property) | Supported States and Properties<http://www.w3.org/TR/wai-aria/states_and_properties#aria-autocomplete>}
		"""
		
		pass