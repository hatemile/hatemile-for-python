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
from hatemile.util.htmldomparser import HTMLDOMParser
from hatemile.util.beautifulsoup.beautifulsouphtmldomelement import BeautifulSoupHTMLDOMElement
import re

class BeautifulSoupHTMLDOMParser(HTMLDOMParser):
    """
    The class BeautifulSoupHTMLDOMParser is official implementation of HTMLDOMParser
    interface for the BeautifulSoup library.
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
            self._fixDataSelect()
        self.results = []
    
    def _inList(self, originalList, item):
        for itemList in originalList:
            if item is itemList:
                return True
        return False
    
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
            if not self._inList(parents, result.parent):
                parents.append(result.parent)
                groups.append([])
                groups[len(groups) - 1].append(result)
            else:
                groups[parents.index(result.parent)].append(result)
        array = []
        for group in groups:
            array += sorted(group, key=lambda element: element.parent.contents.index(element))
        return array
    
    def _fixDataSelect(self):
        elements = self.document.select('*')
        for element in elements:
            attributes = element.attrs.keys()
            for attribute in attributes:
                if bool(re.findall('^data-', attribute)):
                    element[re.sub('data-', 'dataaaaaa', attribute)] = element[attribute]
    
    def _removeDataSelect(self):
        elements = self.document.select('*')
        for element in elements:
            attributes = element.attrs.keys()
            for attribute in attributes:
                if bool(re.findall('^dataaaaaa', attribute)):
                    del(element[attribute])
    
    def find(self, selector):
        if isinstance(selector, BeautifulSoupHTMLDOMElement):
            self.results = [selector.getData()]
        else:
            selector = re.sub('data-', 'dataaaaaa', selector)
            selectors = re.split(',', selector)
            self.results = []
            for sel in selectors:
                results = self.document.select(sel)
                for result in results:
                    if not self._inList(self.results, result):
                        self.results.append(result)
        return self
    
    def findChildren(self, selector):
        lastResults = self.results
        if isinstance(selector, BeautifulSoupHTMLDOMElement):
            for result in lastResults:
                if self._inList(result.children, selector): 
                    self.results[selector.getData()]
                    break
        else:
            selector = re.sub('data-', 'dataaaaaa', selector)
            selectors = re.split(',', selector)
            self.results = []
            for sel in selectors:
                for lastResult in lastResults:
                    results = lastResult.select(sel)
                    for result in results:
                        if (self._inList(lastResult.children, result)) and (not self._inList(self.results, result)):
                            self.results.append(result)
        return self
    
    def findDescendants(self, selector):
        lastResults = self.results
        if isinstance(selector, BeautifulSoupHTMLDOMElement):
            for result in lastResults:
                if self._inList(selector.parents, result):
                    self.results = [selector.getData()]
                    break
        else:
            selector = re.sub('data-', 'dataaaaaa', selector)
            selectors = re.split(',', selector)
            self.results = []
            for sel in selectors:
                for lastResult in lastResults:
                    results = lastResult.select(sel)
                    for result in results:
                        if not self._inList(self.results, result):
                            self.results.append(result)
        return self
    
    def findAncestors(self, selector):
        lastResults = self.results
        if isinstance(selector, BeautifulSoupHTMLDOMElement):
            for result in lastResults:
                if self._inList(result.parents, selector):
                    self.results = [selector.getData()]
                    break
        else:
            parents = []
            self.results = []
            selector = re.sub('data-', 'dataaaaaa', selector)
            selectors = re.split(',', selector)
            for sel in selectors:
                results = self.document.select(sel)
                for result in results:
                    if not self._inList(parents, result):
                        parents.append(result)
            for result in lastResults:
                for parent in parents:
                    if (self._inList(result.parents, parent)) and (not self._inList(self.results, parent)):
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
    
    def listResults(self):
        array = []
        ordenedResults = self._sortResults(self.results)
        for result in ordenedResults:
            array.append(BeautifulSoupHTMLDOMElement(result))
        return array
    
    def createElement(self, tag):
        return BeautifulSoupHTMLDOMElement(self.document.new_tag(tag))
    
    def getHTML(self):
        self._removeDataSelect()
        content = self.document.encode(formatter=None)
        self._fixDataSelect()
        return content
    
    def getParser(self):
        return self.document
    
    def clearParser(self):
        del(self.results[:])
        self.results = None
        self.document = None
