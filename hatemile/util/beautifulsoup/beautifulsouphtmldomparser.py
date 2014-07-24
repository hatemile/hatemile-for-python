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

from bs4 import BeautifulSoup
from hatemile.util import HTMLDOMParser
from . import BeautifulSoupHTMLDOMElement
import re

class BeautifulSoupHTMLDOMParser(HTMLDOMParser):
	"""
	The class BeautifulSoupHTMLDOMParser is official implementation of HTMLDOMParser
	interface for the BeautifulSoup library.
	__version__ = 2014-07-23
	"""
	
	def __init__(self, codeOrParser):
		"""
		Initializes a new object that encapsulate the parser of BeautifulSoup.
		@param codeOrParser: The root element of the parser or the HTML code.
		@type codeOrParser: str or bs4.element.Tag
		"""
		
		if isinstance(codeOrParser, BeautifulSoup):
			self.document = codeOrParser
		else:
			self.document = BeautifulSoup(codeOrParser)
		self.results = []
	
	def _sortResults(self, results):
		"""
		Order the results.
		@param results: The disordened results.
		@type results: array.bs4.element.Tag
		@return: The ordened results.
		@rtype: array.bs4.element.Tag
		"""
		
		parents = []
		groups = []
		for result in results:
			if not result.parent in parents:
				parents.append(result.parent)
				groups.append([])
				groups[len(groups) - 1].append(result)
			else:
				groups[parents.index(result.parent)].append(result)
		array = []
		for group in groups:
			array += sorted(group, key=lambda element: element.parent.contents.index(element))
		return array 
	
	def find(self, selector):
		if isinstance(selector, BeautifulSoupHTMLDOMElement):
			self.results = [selector.getData()]
		else:
			selectors = re.split(',', selector)
			self.results = []
			for sel in selectors:
				results = self.document.select(sel)
				for result in results:
					if result not in self.results:
						self.results.append(result)
		return self
	
	def findChildren(self, selector):
		lastResults = self.results
		if isinstance(selector, BeautifulSoupHTMLDOMElement):
			for result in lastResults:
				if selector in result.children:
					self.results[selector.getData()]
					break
		else:
			selectors = re.split(',', selector)
			self.results = []
			for sel in selectors:
				for lastResult in lastResults:
					results = lastResult.select(sel)
					for result in results:
						if (result in lastResult.children) and (result not in self.results):
							self.results.append(result)
		return self
	
	def findDescendants(self, selector):
		lastResults = self.results
		if isinstance(selector, BeautifulSoupHTMLDOMElement):
			for result in lastResults:
				if result in selector.parents:
					self.results = [selector.getData()]
					break
		else:
			selectors = re.split(',', selector)
			self.results = []
			for sel in selectors:
				for lastResult in lastResults:
					results = lastResult.select(sel)
					for result in results:
						if result not in self.results:
							self.results.append(result)
		return self
	
	def findAncestors(self, selector):
		lastResults = self.results
		if isinstance(selector, BeautifulSoupHTMLDOMElement):
			for result in lastResults:
				if selector in result.parents:
					self.results = [selector.getData()]
					break
		else:
			parents = []
			selectors = re.split(',', selector)
			for sel in selectors:
				results = self.document.select(sel)
				for result in results:
					if result not in parents:
						parents.append(result)
			for result in lastResults:
				for parent in parents:
					if (parent in result.parents) and (parent not in self.results):
						self.results.append(parent)
		return self
	
	def firstResult(self):
		if not bool(self.results):
			return None
		return BeautifulSoupHTMLDOMElement(self.results[0])
	
	def lastResult(self):
		if not bool(self.results):
			return None
		return BeautifulSoupHTMLDOMElement(self.results[len(self.results) - 1])
	
	def listResults(self, mank = False):
		array = []
		ordenedResults = self._sortResults(self.results)
		for result in ordenedResults:
			array.append(BeautifulSoupHTMLDOMElement(result))
		return array
	
	def createElement(self, tag):
		return BeautifulSoupHTMLDOMElement(self.document.new_tag(tag))
	
	def getHTML(self):
		return self.document.encode(formatter=None)
	
	def getParser(self):
		return self.document
	
	def clearParser(self):
		del(self.results[:])
		self.results = None
		self.document = None