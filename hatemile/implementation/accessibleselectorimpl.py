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

from hatemile import AccessibleSelector

class AccessibleSelectorImpl(AccessibleSelector):
	def __init__(self, parser, configure):
		self.parser = parser
		self.changes = configure.getSelectorChanges()
		self.dataIgnore = configure.getParameter('data-ignore')
	def fixSelectors(self):
		for change in self.changes:
			elements = self.parser.find(change.getSelector()).listResults()
			for element in elements:
				if not element.hasAttribute(self.dataIgnore):
					element.setAttribute(change.getAttribute(), change.getValueForAttribute())