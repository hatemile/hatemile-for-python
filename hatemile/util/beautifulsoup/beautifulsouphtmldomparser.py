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
    def __init__(self, code):
        self.document = BeautifulSoup(code)
        self.results = []
    def find(self, selector):
        if isinstance(selector, BeautifulSoupHTMLDOMElement):
            self.results = [selector.getData()]
        else:
            selectors = re.split(',', selector)
            self.results = []
            for sel in selectors:
                results = self.document.select(sel)
                arrayAux = []
                for result in results:
                    if not result in self.results:
                        arrayAux.append(result)
                for itemAux in arrayAux:
                    self.results.append(itemAux)
        return self
    def findChildren(self, selector):
        array = []
        if isinstance(selector, BeautifulSoupHTMLDOMElement):
            for result in self.results:
                if selector in result.children:
                    array.append(selector.getData())
                    break
        else:
            selectors = re.split(',', selector)
            lastResults = self.results
            self.results = []
            for sel in selectors:
                for lastResult in lastResults:
                    results = lastResult.select(sel)
                    arrayAux = []
                    for result in results:
                        if result in lastResult.children and not result in array:
                            arrayAux.append(result)
                    for itemAux in arrayAux:
                        array.append(itemAux)
        self.results = array
        return self
    def findDescendants(self, selector):
        array = []
        if isinstance(selector, BeautifulSoupHTMLDOMElement):
            for result in self.results:
                if result in selector.parents:
                    array.append(selector.getData())
                    break
        else:
            selectors = re.split(',', selector)
            lastResults = self.results
            self.results = []
            for sel in selectors:
                for lastResult in lastResults:
                    results = lastResult.select(sel)
                    arrayAux = []
                    for result in results:
                        if not result in array:
                            arrayAux.append(result)
                    for itemAux in arrayAux:
                        array.append(itemAux)
        self.results = array
        return self
    def findAncestors(self, selector):
        array = []
        if isinstance(selector, BeautifulSoupHTMLDOMElement):
            for result in self.results:
                if selector in result.parents:
                    array.append(selector.getData())
                    break
        else:
            parents = []
            selectors = re.split(',', selector)
            for sel in selectors:
                results = self.document.select(sel)
                for result in results:
                    if not result in parents:
                        parents.append(result)
            for result in self.results:
                for parent in parents:
                    if parent in result.parents and not parent in array:
                        array.append(parent)
        self.results = array
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
    def clearParser(self):
        del(self.results[:])
        self.results = None
        self.document = None
    def _sortResults(self, results):
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