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

    def __init__(self, parser, configure, userAgent=None):
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
        self.prefixId = configure.get_parameter('prefix-generated-ids')
        self.textShortcuts = configure.get_parameter('text-shortcuts')
        self.textHeading = configure.get_parameter('text-heading')
        self.standartPrefix = configure.get_parameter(
            'text-standart-shortcut-prefix'
        )
        self.skippers = configure.get_skippers()
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
            firefox = re.match(
                '.*firefox/[2-9]|minefield/3.*',
                userAgent
            ) is not None
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

    def _get_description(self, element):
        """
        Returns the description of element.
        @param element: The element with description.
        @type element: L{hatemile.util.HTMLDOMElement}
        @return: The description of element.
        @rtype: str
        """

        description = None
        if element.has_attribute('title'):
            description = element.get_attribute('title')
        elif element.has_attribute('aria-label'):
            description = element.get_attribute('aria-label')
        elif element.has_attribute('alt'):
            description = element.get_attribute('alt')
        elif element.has_attribute('label'):
            description = element.get_attribute('label')
        elif (
            (element.has_attribute('aria-labelledby'))
            or (element.has_attribute('aria-describedby'))
        ):
            if element.has_attribute('aria-labelledby'):
                descriptionIds = re.split(
                    '[ \n\r\t]+',
                    element.get_attribute('aria-labelledby').strip()
                )
            else:
                descriptionIds = re.split(
                    '[ \n\r\t]+',
                    element.get_attribute('aria-describedby').strip()
                )
            for descriptionId in descriptionIds:
                elementDescription = self.parser.find(
                    '#' + descriptionId
                ).first_result()
                if elementDescription is not None:
                    description = elementDescription.get_text_content()
                    break
        elif (
            (element.get_tag_name() == 'INPUT')
            and (element.has_attribute('type'))
        ):
            typeAttribute = element.get_attribute('type').lower()
            if (
                (
                    (typeAttribute == 'button')
                    or (typeAttribute == 'submit')
                    or (typeAttribute == 'reset')
                )
                and (element.has_attribute('value'))
            ):
                description = element.get_attribute('value')
        if not bool(description):
            description = element.get_text_content()
        return re.sub('[ \n\r\t]+', ' ', description.strip())

    def _generate_list_shortcuts(self):
        """
        Generate the list of shortcuts of page.
        @return: The list of shortcuts of page.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        container = self.parser.find(
            '#' + self.idContainerShortcuts
        ).first_result()
        htmlList = None
        if container is None:
            local = self.parser.find('body').first_result()
            if local is not None:
                container = self.parser.create_element('div')
                container.set_attribute('id', self.idContainerShortcuts)

                textContainer = self.parser.create_element('span')
                textContainer.set_attribute('id', self.idTextShortcuts)
                textContainer.append_text(self.textShortcuts)

                container.append_element(textContainer)
                local.append_element(container)

                self._execute_fix_skipper(container)
                self._execute_fix_skipper(textContainer)
        if container is not None:
            htmlList = self.parser.find(container).find_children(
                'ul'
            ).first_result()
            if htmlList is None:
                htmlList = self.parser.create_element('ul')
                container.append_element(htmlList)
            self._execute_fix_skipper(htmlList)
        self.listShortcutsAdded = True

        return htmlList

    def _generate_list_skippers(self):
        """
        Generate the list of skippers of page.
        @return: The list of skippers of page.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        container = self.parser.find(
            '#' + self.idContainerSkippers
        ).first_result()
        htmlList = None
        if container is None:
            local = self.parser.find('body').first_result()
            if local is not None:
                container = self.parser.create_element('div')
                container.set_attribute('id', self.idContainerSkippers)
                local.get_first_element_child().insert_before(container)
        if container is not None:
            htmlList = self.parser.find(container).find_children(
                'ul'
            ).first_result()
            if htmlList is None:
                htmlList = self.parser.create_element('ul')
                container.append_element(htmlList)
        self.listSkippersAdded = True

        return htmlList

    def _generate_list_heading(self):
        """
        Generate the list of heading links of page.
        @return: The list of heading links of page.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        container = self.parser.find(
            '#' + self.idContainerHeading
        ).first_result()
        htmlList = None
        if container is None:
            local = self.parser.find('body').first_result()
            if local is not None:
                container = self.parser.create_element('div')
                container.set_attribute('id', self.idContainerHeading)

                textContainer = self.parser.create_element('span')
                textContainer.set_attribute('id', self.idTextHeading)
                textContainer.append_text(self.textHeading)

                container.append_element(textContainer)
                local.append_element(container)

                self._execute_fix_skipper(container)
                self._execute_fix_skipper(textContainer)
        if container is not None:
            htmlList = self.parser.find(container).find_children(
                'ol'
            ).first_result()
            if htmlList is None:
                htmlList = self.parser.create_element('ol')
                container.append_element(htmlList)
            self._execute_fix_skipper(htmlList)
        return htmlList

    def _get_heading_level(self, element):
        """
        Returns the level of heading.
        @param element: The heading.
        @type element: L{hatemile.util.HTMLDOMElement}
        @return: The level of heading.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        tag = element.get_tag_name()
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

    def _is_valid_heading(self):
        """
        Inform if the headings of page are sintatic correct.
        @return: True if the headings of page are sintatic correct or false if
        not.
        @rtype: bool
        """

        elements = self.parser.find('h1,h2,h3,h4,h5,h6').list_results()
        lastLevel = 0
        countMainHeading = 0
        self.validateHeading = True
        for element in elements:
            level = self._get_heading_level(element)
            if level == 1:
                if countMainHeading == 1:
                    return False
                else:
                    countMainHeading = 1
            if (level - lastLevel) > 1:
                return False
            lastLevel = level
        return True

    def _generate_anchor_for(self, element, dataAttribute, anchorClass):
        """
        Generate an anchor for the element.
        @param element: The element.
        @type element: L{hatemile.util.HTMLDOMElement}
        @param dataAttribute: The name of attribute that links the element with
        the anchor.
        @type dataAttribute: str
        @param anchorClass: The HTML class of anchor.
        @type anchorClass: str
        @return: The anchor.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        CommonFunctions.generate_id(element, self.prefixId)
        if self.parser.find(
            '[' + dataAttribute + '="' + element.get_attribute('id') + '"]'
        ).first_result() is None:
            if element.get_tag_name() == 'A':
                anchor = element
            else:
                anchor = self.parser.create_element('a')
                CommonFunctions.generate_id(anchor, self.prefixId)
                anchor.set_attribute('class', anchorClass)
                element.insert_before(anchor)
            if not anchor.has_attribute('name'):
                anchor.set_attribute('name', anchor.get_attribute('id'))
            anchor.set_attribute(dataAttribute, element.get_attribute('id'))
        return anchor

    def _free_shortcut(self, shortcut):
        """
        Replace the shortcut of elements, that has the shortcut passed.
        @param shortcut: The shortcut.
        @type shortcut: str
        """

        alphaNumbers = '1234567890abcdefghijklmnopqrstuvwxyz'
        elements = self.parser.find('[accesskey]').list_results()
        found = False
        for element in elements:
            shortcuts = element.get_attribute('accesskey').lower()
            if CommonFunctions.in_list(shortcuts, shortcut):
                for i in range(0, alphaNumbers.length()):
                    key = alphaNumbers[i]
                    found = True
                    for elementWithShortcuts in elements:
                        shortcuts = elementWithShortcuts.get_attribute(
                            'accesskey'
                        ).lower()
                        if CommonFunctions.in_list(shortcuts, key):
                            found = False
                            break
                    if found:
                        element.set_attribute('accesskey', key)
                        break
                if found:
                    break

    def _execute_fix_skipper(self, element):
        """
        Call fixSkipper method for element, if the page has the container of
        skippers.
        @param element: The element.
        @type element: L{hatemile.util.HTMLDOMElement}
        """

        if self.listSkippers is not None:
            for skipper in self.skippers:
                if element in self.parser.find(
                    skipper.get_selector()
                ).list_results():
                    self.fix_skipper(element, skipper)

    def _execute_fix_shortcut(self, element):
        """
        Call fixShortcut method for element, if the page has the container of
        shortcuts.
        @param element: The element.
        @type element: L{hatemile.util.HTMLDOMElement}
        """

        if self.listShortcuts is not None:
            self.fix_shortcut(element)

    def fix_shortcut(self, element):
        if element.has_attribute('accesskey'):
            description = self._get_description(element)
            if not element.has_attribute('title'):
                element.set_attribute('title', description)

            if not self.listShortcutsAdded:
                self.listShortcuts = self._generate_list_shortcuts()

            if self.listShortcuts is not None:
                keys = re.split(
                    '[ \n\t\r]+',
                    element.get_attribute('accesskey')
                )
                for key in keys:
                    key = key.upper()
                    if self.parser.find(self.listShortcuts).find_children(
                        '[' + self.dataAccessKey + '="' + key + '"]'
                    ).first_result() is None:
                        item = self.parser.create_element('li')
                        item.set_attribute(self.dataAccessKey, key)
                        item.append_text(
                            self.prefix
                            + ' + '
                            + key
                            + ': '
                            + description
                        )
                        self.listShortcuts.append_element(item)

    def fix_shortcuts(self):
        elements = self.parser.find('[accesskey]').list_results()
        for element in elements:
            if not element.has_attribute(self.dataIgnore):
                self.fix_shortcut(element)

    def fix_skipper(self, element, skipper):
        if not self.listSkippersAdded:
            self.listSkippers = self._generate_list_skippers()
        if self.listSkippers is not None:
            anchor = self._generate_anchor_for(
                element,
                self.dataAnchorFor,
                self.classSkipperAnchor
            )
            if anchor is not None:
                itemLink = self.parser.create_element('li')
                link = self.parser.create_element('a')
                link.set_attribute('href', '#' + anchor.get_attribute('name'))
                link.append_text(skipper.get_default_text())

                shortcuts = skipper.get_shortcuts()
                if (len(shortcuts) != 0):
                    shortcut = shortcuts[0]
                    if shortcut != '':
                        self._free_shortcut(shortcut)
                        link.set_attribute('accesskey', shortcut)
                CommonFunctions.generate_id(link, self.prefixId)

                itemLink.append_element(link)
                self.listSkippers.append_element(itemLink)

                self._execute_fix_shortcut(link)

    def fix_skippers(self):
        i = 0
        for skipper in self.skippers:
            elements = self.parser.find(skipper.get_selector()).list_results()
            count = len(elements) > 1
            if count:
                i = 1
            shortcuts = skipper.get_shortcuts()
            for element in elements:
                if not element.has_attribute(self.dataIgnore):
                    if count:
                        defaultText = skipper.get_default_text() + " " + str(i)
                        i = i + 1
                    else:
                        defaultText = skipper.get_default_text()
                    if len(shortcuts) > 0:
                        self.fix_skipper(
                            element,
                            Skipper(
                                skipper.get_selector(),
                                defaultText,
                                shortcuts.pop()
                            )
                        )
                    else:
                        self.fix_skipper(
                            element,
                            Skipper(
                                skipper.get_selector(),
                                defaultText,
                                ''
                            )
                        )

    def fix_heading(self, element):
        if not self.validateHeading:
            self.validHeading = self._is_valid_heading()
        if self.validHeading:
            anchor = self._generate_anchor_for(
                element,
                self.dataHeadingAnchorFor,
                self.classHeadingAnchor
            )
            if anchor is not None:
                listElement = None
                level = self._get_heading_level(element)
                if level == 1:
                    listElement = self._generate_list_heading()
                else:
                    superItem = self.parser.find(
                        '#'
                        + self.idContainerHeading
                    ).find_descendants(
                        '['
                        + self.dataHeadingLevel
                        + '="'
                        + str(level - 1)
                        + '"]'
                    ).last_result()
                    if superItem is not None:
                        listElement = self.parser.find(
                            superItem
                        ).find_children('ol').first_result()
                        if listElement is None:
                            listElement = self.parser.create_element('ol')
                            superItem.append_element(listElement)
                if listElement is not None:
                    item = self.parser.create_element('li')
                    item.set_attribute(self.dataHeadingLevel, str(level))

                    link = self.parser.create_element('a')
                    link.set_attribute(
                        'href',
                        '#' + anchor.get_attribute('name')
                    )
                    link.append_text(element.get_text_content())

                    item.append_element(link)
                    listElement.append_element(item)

    def fix_headings(self):
        elements = self.parser.find('h1,h2,h3,h4,h5,h6').list_results()
        for element in elements:
            if not element.has_attribute(self.dataIgnore):
                self.fix_heading(element)
