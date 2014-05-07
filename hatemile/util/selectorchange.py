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

class SelectorChange:
	def __init__(self, selector = None, attribute = None, valueForAttribute = None):
		self.selector = selector
		self.attribute = attribute
		self.valueForAttribute = valueForAttribute
	
	def getSelector(self):
		return self.selector
	
	def setSelector(self, selector):
		self.selector = selector
		
	def getAttribute(self):
		return self.attribute
	
	def setAttribute(self, attribute):
		self.attribute = attribute
	
	def getValueForAttribute(self):
		return self.valueForAttribute
	
	def setValueForAttribute(self, valueForAttribute):
		self.valueForAttribute = valueForAttribute