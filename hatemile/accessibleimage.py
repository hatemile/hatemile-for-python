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

class AccessibleImage:
	"""
	The AccessibleImage interface fix the problems of accessibility associated
	with the images.
	__version__ = 2014-07-23
	"""
	
	def fixMap(self, elementMap):
		"""
		Fix the map of images.
		@param elementMap: The map of images.
		@type elementMap: L{hatemile.util.HTMLDOMElement}
		@see: U{WCAG 1.0 Checkpoint 1.5<http://www.w3.org/TR/WAI-WEBCONTENT-TECHS/#tech-redundant-client-links>}
		"""
		
		pass
	
	def fixMaps(self):
		"""
		Fix the maps of images.
		@see: U{WCAG 1.0 Checkpoint 1.5<http://www.w3.org/TR/WAI-WEBCONTENT-TECHS/#tech-redundant-client-links>}
		"""
		
		pass
	
	def fixLongDescription(self, element):
		"""
		Fix the element with long description.
		@param element: The element with long description.
		@type element: L{hatemile.util.HTMLDOMElement}
		@see: U{G73: Providing a long description in another location with a link to it that is immediately adjacent to the non-text content<http://www.w3.org/TR/WCAG20-TECHS/G73.html>}
		@see: U{G74: Providing a long description in text near the non-text content, with a reference to the location of the long description in the short description<http://www.w3.org/TR/WCAG20-TECHS/G74.html>}
		"""
		
		pass
	
	def fixLongDescriptions(self):
		"""
		Fix the elements with longs descriptions.
		@see: U{G73: Providing a long description in another location with a link to it that is immediately adjacent to the non-text content<http://www.w3.org/TR/WCAG20-TECHS/G73.html>}
		@see: U{G74: Providing a long description in text near the non-text content, with a reference to the location of the long description in the short description<http://www.w3.org/TR/WCAG20-TECHS/G74.html>}
		"""
		
		pass