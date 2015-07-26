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

from bs4 import BeautifulSoup
from bs4 import PageElement
from hatemile.util import HTMLDOMElement
import copy, re

class BeautifulSoupHTMLDOMElement(HTMLDOMElement):
	"""
	The BeautifulSoupHTMLDOMElement class is official implementation of HTMLDOMElement
	interface for the BeautifulSoup library.
	"""
	
	def __init__(self, element):
		"""
		Initializes a new object that encapsulate the BeautifulSoup Tag.
		@param element: The BeautifulSoup Tag.
		@type element: bs4.element.Tag
		"""
		
		self.data = element
	
	def getTagName(self):
		return self.data.name.upper()
	
	def getAttribute(self, name):
		if not self.hasAttribute(name):
			return None
		if type(self.data[name]) == type([]):
			array = self.data[name]
			value = ''
			for item in array:
				value += item + ' '
			return value.strip()
		else:
			return self.data[name]
	
	def setAttribute(self, name, value):
		self.data[name] = value
		if bool(re.findall('^data-', name)):
			self.data[re.sub('^data-', 'dataaaaaa', name)] = value
	
	def removeAttribute(self, name):
		if self.hasAttribute(name):
			del(self.data[name])
			if bool(re.findall('^data-', name)):
				del(self.data[re.sub('^data-', 'dataaaaaa', name)])
	
	def hasAttribute(self, name):
		return self.data.has_attr(name)
	
	def hasAttributes(self):
		return bool(self.data.attrs)
	
	def getTextContent(self):
		return self.data.get_text()
	
	def insertBefore(self, newElement):
		self.data.insert_before(newElement.getData())
		return newElement
	
	def insertAfter(self, newElement):
		self.data.insert_after(newElement.getData())
		return newElement
	
	def removeElement(self):
		self.data.extract()
		return self
	
	def replaceElement(self, newElement):
		self.data.replace_with(newElement.getData())
		return newElement
	
	def appendElement(self, element):
		self.data.append(element.getData())
		return element
	
	def getChildren(self):
		array = []
		for child in self.data.children:
			if isinstance(child, PageElement):
				array.append(BeautifulSoupHTMLDOMElement(child))
		return array
	
	def appendText(self, text):
		self.data.append(text)
	
	def hasChildren(self):
		return bool(self.getChildren())
	
	def getParentElement(self):
		return BeautifulSoupHTMLDOMElement(self.data.parent)
	
	def getInnerHTML(self):
		string = ''
		for child in self.data.children:
			string += str(child)
		return string
	
	def setInnerHTML(self, html):
		documentAuxiliar = BeautifulSoup(html, 'html.parser')
		children = []
		for child in self.data.children:
			children.append(child)
		for child in children:
			child.extract()
		for child in documentAuxiliar.children:
			self.data.append(child)
	
	def getOuterHTML(self):
		return str(self.data)
	
	def getData(self):
		return self.data
	
	def setData(self, data):
		self.data = data
	
	def cloneElement(self):
		return BeautifulSoupHTMLDOMElement(copy.copy(self.data))
	
	def getFirstElementChild(self):
		if not self.hasChildren():
			return None
		for child in self.data.children:
			if isinstance(child, PageElement):
				return BeautifulSoupHTMLDOMElement(child)
		return None
	
	def getLastElementChild(self):
		if not self.hasChildren():
			return None
		lastValue = None
		for child in self.data.children:
			if isinstance(child, PageElement):
				lastValue = child
		if lastValue != None:
			return BeautifulSoupHTMLDOMElement(lastValue)
		return None