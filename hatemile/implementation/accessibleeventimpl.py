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
from hatemile import AccessibleEvent

class AccessibleEventImpl(AccessibleEvent):
	"""
	The AccessibleEventImpl class is official implementation of AccessibleEvent
	interface.
	__version__ = 2014-07-23
	"""
	
	def __init__(self, parser, configure):
		"""
		Initializes a new object that manipulate the accessibility of the
		Javascript events of elements of parser.
		@param parser: The HTML parser.
		@type parser: L{hatemile.util.HTMLDOMParser}
		@param configure: The configuration of HaTeMiLe.
		@type configure: L{hatemile.util.Configure}
		"""
		
		self.parser = parser
		self.prefixId = configure.getParameter('prefix-generated-ids')
		self.idScriptEvent = configure.getParameter('id-script-event')
		self.idListIdsScriptOnActive = configure.getParameter('id-list-ids-script-onactive')
		self.idFunctionScriptFixOnActive = configure.getParameter('id-function-script-fix-onactive')
		self.dataIgnore = 'data-' + configure.getParameter('data-ignore')
		self.mainScriptAdded = False
		self.otherScriptsAdded = False
		self.scriptList = None
	
	def _generateMainScript(self):
		"""
		Generate the main script in parser.
		"""
		
		local = self.parser.find('head').firstResult()
		if local == None:
			local = self.parser.find('body').firstResult()
		if (local != None) and (self.parser.find('#' + self.idScriptEvent).firstResult() == None):
			script = self.parser.createElement('script')
			script.setAttribute('id', self.idScriptEvent)
			script.setAttribute('type', 'text/javascript')
			javascript = 'function onFocusEvent(e){if(e.onmouseover!=undefined){try{e.onmouseover();}catch(x){}}}function onBlurEvent(e){if(e.onmouseout!=undefined){try{e.onmouseout();}catch(x){}}}function isEnter(k){var n="\\n".charCodeAt(0);var r="\\r".charCodeAt(0);return ((k==n)||(k==r));}function onKeyDownEvent(l,v){if(isEnter(v.keyCode)&&(l.onmousedown!=undefined)){try{l.onmousedown();}catch(x){}}}function onKeyPressEvent(l,v){if(isEnter(v.keyCode)){if(l.onclick!=undefined){try{l.click();}catch(x){}}else if(l.ondblclick!=undefined){try{l.ondblclick();}catch(x){}}}}function onKeyUpEvent(l,v){if(isEnter(v.keyCode)&&(l.onmouseup!=undefined)){try{l.onmouseup();}catch(x){}}}'
			script.appendText(javascript)
			local.appendElement(script)
		self.mainScriptAdded = True
	
	def _generateOtherScripts(self):
		"""
		Generate the other scripts in parser.
		"""
		
		local = self.parser.find('body').firstResult()
		if local != None:
			self.scriptList = self.parser.find('#' + self.idListIdsScriptOnActive).firstResult()
			if self.scriptList == None:
				self.scriptList = self.parser.createElement('script')
				self.scriptList.setAttribute('id', self.idListIdsScriptOnActive)
				self.scriptList.setAttribute('type', 'text/javascript')
				self.scriptList.appendText('var s=[];')
				local.appendElement(self.scriptList)
			if self.parser.find('#' + self.idFunctionScriptFixOnActive).firstResult() == None:
				scriptFunction = self.parser.createElement('script')
				scriptFunction.setAttribute('id', self.idFunctionScriptFixOnActive)
				scriptFunction.setAttribute('type', 'text/javascript')
				javascript = 'var e;for(var i=0,l=s.length;i<l;i++){e=document.getElementById(s[i]);if(e.onkeypress==undefined){e.onkeypress=function(v){onKeyPressEvent(e,v);};}if(e.onkeyup==undefined){e.onkeyup=function(v){onKeyUpEvent(e,v);};}if(e.onkeydown==undefined){e.onkeydown=function(v){onKeyDownEvent(e,v);};}}'
				scriptFunction.appendText(javascript)
				local.appendElement(scriptFunction)
		self.otherScriptsAdded = True
	
	def _addEventInElement(self, element):
		"""
		Add the id of element in list of elements that will have its events
		modified.
		@param element: The element with id.
		@type element: L{hatemile.util.HTMLDOMElement}
		"""
		
		if not self.otherScriptsAdded:
			self._generateOtherScripts()
		
		if self.scriptList != None:
			CommonFunctions.generateId(element, self.prefixId)
			self.scriptList.appendText("s.push('" + element.getAttribute('id') + "');")
		else:
			if not element.hasAttribute('onkeypress'):
				element.setAttribute('onkeypress', 'try{onKeyPressEvent(this,event);}catch(x){}')
			if not element.hasAttribute('onkeyup'):
				element.setAttribute('onkeyup', 'try{onKeyUpEvent(this,event);}catch(x){}')
			if not element.hasAttribute('onkeydown'):
				element.setAttribute('onkeydown', 'try{onKeyDownEvent(this,event);}catch(x){}')
	
	def fixOnHover(self, element):
		tag = element.getTagName()
		if not ((tag == 'INPUT') or (tag == 'BUTTON') or (tag == 'A') or (tag == 'SELECT') or (tag == 'TEXTAREA') or (element.hasAttribute('tabindex'))):
			element.setAttribute('tabindex', '0')
		
		if not self.mainScriptAdded:
			self._generateMainScript()
		
		if not element.hasAttribute('onfocus'):
			element.setAttribute('onfocus', 'onFocusEvent(this);')
		if not element.hasAttribute('onblur'):
			element.setAttribute('onblur', 'onBlurEvent(this);')
	
	def fixOnHovers(self):
		elements = self.parser.find('[onmouseover],[onmouseout]').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixOnHover(element)
	
	def fixOnActive(self, element):
		tag = element.getTagName()
		if not ((tag == 'INPUT') or (tag == 'BUTTON') or (tag == 'A')):
			if not ((element.hasAttribute('tabindex')) or (tag == 'SELECT') or (tag == 'TEXTAREA')):
				element.setAttribute('tabindex', '0')
			
			if not self.mainScriptAdded:
				self._generateMainScript()
			
			self._addEventInElement(element)
	
	def fixOnActives(self):
		elements = self.parser.find('[onclick],[onmousedown],[onmouseup],[ondblclick]').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixOnActive(element)