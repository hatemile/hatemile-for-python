# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from hatemile.accessiblenavigation import AccessibleNavigation
import re
from hatemile.util.commonfunctions import CommonFunctions
from hatemile.util.skipper import Skipper


class AccessibleNavigationImplementation(AccessibleNavigation):
    """
    The AccessibleNavigationImplementation class is official implementation of
    AccessibleNavigation interface.
    """

    def __init__(self, parser, configure, userAgent = None):
        """
        Initializes a new object that manipulate the accessibility of the
        navigation of parser.
        @param parser: The HTML parser.
        @type parser: L{hatemile.util.HTMLDOMParser}
        @param configure: The configuration of HaTeMiLe.
        @type configure: L{hatemile.util.Configure}
        @param userAgent: The user agent of the user.
        @type userAgent: str
        """

        self.parser = parser
        self.idContainerShortcuts = 'container-shortcuts'
        self.idContainerSkippers = 'container-skippers'
        self.idContainerHeading = 'container-heading'
        self.idTextShortcuts = 'text-shortcuts'
        self.idTextHeading = 'text-heading'
        self.classSkipperAnchor = 'skipper-anchor'
        self.classHeadingAnchor = 'heading-anchor'
        self.dataAccessKey = 'data-shortcutdescriptionfor'
        self.dataIgnore = 'data-ignoreaccessibilityfix'
        self.dataAnchorFor = 'data-anchorfor'
        self.dataHeadingAnchorFor = 'data-headinganchorfor'
        self.dataHeadingLevel = 'data-headinglevel'
        self.prefixId = configure.getParameter('prefix-generated-ids')
        self.textShortcuts = configure.getParameter('text-shortcuts')
        self.textHeading = configure.getParameter('text-heading')
        self.standartPrefix = configure.getParameter('text-standart-shortcut-prefix')
        self.skippers = configure.getSkippers()
        self.listShortcutsAdded = False
        self.listSkippersAdded = False
        self.validateHeading = False
        self.validHeading = False
        self.listSkippers = None
        self.listShortcuts = None

        if userAgent is not None:
            userAgent = userAgent.lower()
            opera = 'opera' in userAgent
            mac = 'mac' in userAgent
            konqueror = 'konqueror' in userAgent
            spoofer = 'spoofer' in userAgent
            safari = 'applewebkit' in userAgent
            windows = 'windows' in userAgent
            chrome = 'chrome' in userAgent
            firefox = re.match('.*firefox/[2-9]|minefield/3.*', userAgent) is not None
            ie = ('msie' in userAgent) or ('trident' in userAgent)

            if opera:
                self.prefix = 'SHIFT + ESC'
            elif chrome and mac and (not spoofer):
                self.prefix = 'CTRL + OPTION'
            elif safari and (not windows) and (not spoofer):
                self.prefix = 'CTRL + ALT'
            elif (not windows) and (safari or mac or konqueror):
                self.prefix = 'CTRL'
            elif firefox:
                self.prefix = 'ALT + SHIFT'
            elif chrome or ie:
                self.prefix = 'ALT'
            else:
                self.prefix = self.standartPrefix
        else:
            self.prefix = self.standartPrefix

    def _getDescription(self, element):
        """
        Returns the description of element.
        @param element: The element with description.
        @type element: L{hatemile.util.HTMLDOMElement}
        @return: The description of element.
        @rtype: str
        """

        description = None
        if element.hasAttribute('title'):
            description = element.getAttribute('title')
        elif element.hasAttribute('aria-label'):
            description = element.getAttribute('aria-label')
        elif element.hasAttribute('alt'):
            description = element.getAttribute('alt')
        elif element.hasAttribute('label'):
            description = element.getAttribute('label')
        elif (element.hasAttribute('aria-labelledby')) or (element.hasAttribute('aria-describedby')):
            if element.hasAttribute('aria-labelledby'):
                descriptionIds = re.split('[ \n\r\t]+', element.getAttribute('aria-labelledby').strip())
            else:
                descriptionIds = re.split('[ \n\r\t]+', element.getAttribute('aria-describedby').strip())
            for descriptionId in descriptionIds:
                elementDescription = self.parser.find('#' + descriptionId).firstResult()
                if elementDescription is not None:
                    description = elementDescription.getTextContent()
                    break
        elif (element.getTagName() == 'INPUT') and (element.hasAttribute('type')):
            typeAttribute = element.getAttribute('type').lower()
            if ((typeAttribute == 'button') or (typeAttribute == 'submit') or (typeAttribute == 'reset')) and (element.hasAttribute('value')):
                description = element.getAttribute('value')
        if not bool(description):
            description = element.getTextContent()
        return re.sub('[ \n\r\t]+', ' ', description.strip())

    def _generateListShortcuts(self):
        """
        Generate the list of shortcuts of page.
        @return: The list of shortcuts of page.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        container = self.parser.find('#' + self.idContainerShortcuts).firstResult()
        htmlList = None
        if container is None:
            local = self.parser.find('body').firstResult()
            if local is not None:
                container = self.parser.createElement('div')
                container.setAttribute('id', self.idContainerShortcuts)

                textContainer = self.parser.createElement('span')
                textContainer.setAttribute('id', self.idTextShortcuts)
                textContainer.appendText(self.textShortcuts)

                container.appendElement(textContainer)
                local.appendElement(container)

                self._executeFixSkipper(container)
                self._executeFixSkipper(textContainer)
        if container is not None:
            htmlList = self.parser.find(container).findChildren('ul').firstResult()
            if htmlList is None:
                htmlList = self.parser.createElement('ul')
                container.appendElement(htmlList)
            self._executeFixSkipper(htmlList)
        self.listShortcutsAdded = True

        return htmlList

    def _generateListSkippers(self):
        """
        Generate the list of skippers of page.
        @return: The list of skippers of page.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        container = self.parser.find('#' + self.idContainerSkippers).firstResult()
        htmlList = None
        if container is None:
            local = self.parser.find('body').firstResult()
            if local is not None:
                container = self.parser.createElement('div')
                container.setAttribute('id', self.idContainerSkippers)
                local.getFirstElementChild().insertBefore(container)
        if container is not None:
            htmlList = self.parser.find(container).findChildren('ul').firstResult()
            if htmlList is None:
                htmlList = self.parser.createElement('ul')
                container.appendElement(htmlList)
        self.listSkippersAdded = True

        return htmlList

    def _generateListHeading(self):
        """
        Generate the list of heading links of page.
        @return: The list of heading links of page.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        container = self.parser.find('#' + self.idContainerHeading).firstResult()
        htmlList = None
        if container is None:
            local = self.parser.find('body').firstResult()
            if local is not None:
                container = self.parser.createElement('div')
                container.setAttribute('id', self.idContainerHeading)

                textContainer = self.parser.createElement('span')
                textContainer.setAttribute('id', self.idTextHeading)
                textContainer.appendText(self.textHeading)

                container.appendElement(textContainer)
                local.appendElement(container)

                self._executeFixSkipper(container)
                self._executeFixSkipper(textContainer)
        if container is not None:
            htmlList = self.parser.find(container).findChildren('ol').firstResult()
            if htmlList is None:
                htmlList = self.parser.createElement('ol')
                container.appendElement(htmlList)
            self._executeFixSkipper(htmlList)
        return htmlList

    def _getHeadingLevel(self, element):
        """
        Returns the level of heading.
        @param element: The heading.
        @type element: L{hatemile.util.HTMLDOMElement}
        @return: The level of heading.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        tag = element.getTagName()
        if tag == 'H1':
            return 1
        elif tag == 'H2':
            return 2
        elif tag == 'H3':
            return 3
        elif tag == 'H4':
            return 4
        elif tag == 'H5':
            return 5
        elif tag == 'H6':
            return 6
        else:
            return -1

    def _isValidHeading(self):
        """
        Inform if the headings of page are sintatic correct.
        @return: True if the headings of page are sintatic correct or false if not.
        @rtype: bool
        """

        elements = self.parser.find('h1,h2,h3,h4,h5,h6').listResults()
        lastLevel = 0
        countMainHeading = 0
        self.validateHeading = True
        for element in elements:
            level = self._getHeadingLevel(element)
            if level == 1:
                if countMainHeading == 1:
                    return False
                else:
                    countMainHeading = 1
            if (level - lastLevel) > 1:
                return False
            lastLevel = level
        return True

    def _generateAnchorFor(self, element, dataAttribute, anchorClass):
        """
        Generate an anchor for the element.
        @param element: The element.
        @type element: L{hatemile.util.HTMLDOMElement}
        @param dataAttribute: The name of attribute that links the element with the anchor.
        @type dataAttribute: str
        @param anchorClass: The HTML class of anchor.
        @type anchorClass: str
        @return: The anchor.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        CommonFunctions.generateId(element, self.prefixId)
        if self.parser.find('[' + dataAttribute + '="' + element.getAttribute('id') + '"]').firstResult() is None:
            if element.getTagName() == 'A':
                anchor = element
            else:
                anchor = self.parser.createElement('a')
                CommonFunctions.generateId(anchor, self.prefixId)
                anchor.setAttribute('class', anchorClass)
                element.insertBefore(anchor)
            if not anchor.hasAttribute('name'):
                anchor.setAttribute('name', anchor.getAttribute('id'))
            anchor.setAttribute(dataAttribute, element.getAttribute('id'))
        return anchor

    def _freeShortcut(self, shortcut):
        """
        Replace the shortcut of elements, that has the shortcut passed.
        @param shortcut: The shortcut.
        @type shortcut: str
        """

        alphaNumbers = '1234567890abcdefghijklmnopqrstuvwxyz'
        elements = self.parser.find('[accesskey]').listResults()
        found = False
        for element in elements:
            shortcuts = element.getAttribute('accesskey').lower()
            if CommonFunctions.inList(shortcuts, shortcut):
                for i in range(0, alphaNumbers.length()):
                    key = alphaNumbers[i]
                    found = True
                    for elementWithShortcuts in elements:
                        shortcuts = elementWithShortcuts.getAttribute('accesskey').lower()
                        if CommonFunctions.inList(shortcuts, key):
                            found = False
                            break
                    if found:
                        element.setAttribute('accesskey', key)
                        break
                if found:
                    break

    def _executeFixSkipper(self, element):
        """
        Call fixSkipper method for element, if the page has the container of skippers.
        @param element: The element.
        @type element: L{hatemile.util.HTMLDOMElement}
        """

        if self.listSkippers is not None:
            for skipper in self.skippers:
                if element in self.parser.find(skipper.getSelector()).listResults():
                    self.fixSkipper(element, skipper)

    def _executeFixShortcut(self, element):
        """
        Call fixShortcut method for element, if the page has the container of shortcuts.
        @param element: The element.
        @type element: L{hatemile.util.HTMLDOMElement}
        """

        if self.listShortcuts is not None:
            self.fixShortcut(element)

    def fixShortcut(self, element):
        if element.hasAttribute('accesskey'):
            description = self._getDescription(element)
            if not element.hasAttribute('title'):
                element.setAttribute('title', description)

            if not self.listShortcutsAdded:
                self.listShortcuts = self._generateListShortcuts()

            if self.listShortcuts is not None:
                keys = re.split('[ \n\t\r]+', element.getAttribute('accesskey'))
                for key in keys:
                    key = key.upper()
                    if self.parser.find(self.listShortcuts).findChildren('[' + self.dataAccessKey + '="' + key + '"]').firstResult() is None:
                        item = self.parser.createElement('li')
                        item.setAttribute(self.dataAccessKey, key)
                        item.appendText(self.prefix + ' + ' + key + ': ' + description)
                        self.listShortcuts.appendElement(item)

    def fixShortcuts(self):
        elements = self.parser.find('[accesskey]').listResults()
        for element in elements:
            if not element.hasAttribute(self.dataIgnore):
                self.fixShortcut(element)

    def fixSkipper(self, element, skipper):
        if not self.listSkippersAdded:
            self.listSkippers = self._generateListSkippers()
        if self.listSkippers is not None:
            anchor = self._generateAnchorFor(element, self.dataAnchorFor, self.classSkipperAnchor)
            if anchor is not None:
                itemLink = self.parser.createElement('li')
                link = self.parser.createElement('a')
                link.setAttribute('href', '#' + anchor.getAttribute('name'))
                link.appendText(skipper.getDefaultText())

                shortcuts = skipper.getShortcuts()
                if (len(shortcuts) != 0):
                    shortcut = shortcuts[0]
                    if shortcut != '':
                        self._freeShortcut(shortcut)
                        link.setAttribute('accesskey', shortcut)
                CommonFunctions.generateId(link, self.prefixId)

                itemLink.appendElement(link)
                self.listSkippers.appendElement(itemLink)

                self._executeFixShortcut(link)

    def fixSkippers(self):
        i = 0
        for skipper in self.skippers:
            elements = self.parser.find(skipper.getSelector()).listResults()
            count = len(elements) > 1
            if count:
                i = 1
            shortcuts = skipper.getShortcuts()
            for element in elements:
                if not element.hasAttribute(self.dataIgnore):
                    if count:
                        defaultText = skipper.getDefaultText() + " " + str(i)
                        i = i + 1
                    else:
                        defaultText = skipper.getDefaultText()
                    if len(shortcuts) > 0:
                        self.fixSkipper(element, Skipper(skipper.getSelector(), defaultText, shortcuts.pop()))
                    else:
                        self.fixSkipper(element, Skipper(skipper.getSelector(), defaultText, ''))

    def fixHeading(self, element):
        if not self.validateHeading:
            self.validHeading = self._isValidHeading()
        if self.validHeading:
            anchor = self._generateAnchorFor(element, self.dataHeadingAnchorFor, self.classHeadingAnchor)
            if anchor is not None:
                listElement = None
                level = self._getHeadingLevel(element)
                if level == 1:
                    listElement = self._generateListHeading()
                else:
                    superItem = self.parser.find('#' + self.idContainerHeading).findDescendants('[' + self.dataHeadingLevel + '="' + str(level - 1) + '"]').lastResult()
                    if superItem is not None:
                        listElement = self.parser.find(superItem).findChildren('ol').firstResult()
                        if listElement is None:
                            listElement = self.parser.createElement('ol')
                            superItem.appendElement(listElement)
                if listElement is not None:
                    item = self.parser.createElement('li')
                    item.setAttribute(self.dataHeadingLevel, str(level))

                    link = self.parser.createElement('a')
                    link.setAttribute('href', '#' + anchor.getAttribute('name'))
                    link.appendText(element.getTextContent())

                    item.appendElement(link)
                    listElement.appendElement(item)

    def fixHeadings(self):
        elements = self.parser.find('h1,h2,h3,h4,h5,h6').listResults()
        for element in elements:
            if not element.hasAttribute(self.dataIgnore):
                self.fixHeading(element)
