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

    def __init__(self, parser, configure, user_agent=None):
        """
        Initializes a new object that manipulate the accessibility of the
        navigation of parser.
        @param parser: The HTML parser.
        @type parser: L{hatemile.util.HTMLDOMParser}
        @param configure: The configuration of HaTeMiLe.
        @type configure: L{hatemile.util.Configure}
        @param user_agent: The user agent of the user.
        @type user_agent: str
        """

        self.parser = parser
        self.id_container_shortcuts = 'container-shortcuts'
        self.id_container_skippers = 'container-skippers'
        self.id_container_heading = 'container-heading'
        self.id_text_shortcuts = 'text-shortcuts'
        self.id_text_heading = 'text-heading'
        self.class_skipper_anchor = 'skipper-anchor'
        self.class_heading_anchor = 'heading-anchor'
        self.data_access_key = 'data-shortcutdescriptionfor'
        self.data_ignore = 'data-ignoreaccessibilityfix'
        self.data_anchor_for = 'data-anchorfor'
        self.data_heading_anchor_for = 'data-headinganchorfor'
        self.data_heading_level = 'data-headinglevel'
        self.prefix_id = configure.get_parameter('prefix-generated-ids')
        self.text_shortcuts = configure.get_parameter('text-shortcuts')
        self.text_heading = configure.get_parameter('text-heading')
        self.standart_prefix = configure.get_parameter(
            'text-standart-shortcut-prefix'
        )
        self.skippers = configure.get_skippers()
        self.list_shortcuts_added = False
        self.list_skippers_added = False
        self.validate_heading = False
        self.valid_heading = False
        self.list_skippers = None
        self.list_shortcuts = None

        if user_agent is not None:
            user_agent = user_agent.lower()
            opera = 'opera' in user_agent
            mac = 'mac' in user_agent
            konqueror = 'konqueror' in user_agent
            spoofer = 'spoofer' in user_agent
            safari = 'applewebkit' in user_agent
            windows = 'windows' in user_agent
            chrome = 'chrome' in user_agent
            firefox = re.match(
                '.*firefox/[2-9]|minefield/3.*',
                user_agent
            ) is not None
            ie = ('msie' in user_agent) or ('trident' in user_agent)

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
                self.prefix = self.standart_prefix
        else:
            self.prefix = self.standart_prefix

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
            '#' + self.id_container_shortcuts
        ).first_result()
        htmlList = None
        if container is None:
            local = self.parser.find('body').first_result()
            if local is not None:
                container = self.parser.create_element('div')
                container.set_attribute('id', self.id_container_shortcuts)

                textContainer = self.parser.create_element('span')
                textContainer.set_attribute('id', self.id_text_shortcuts)
                textContainer.append_text(self.text_shortcuts)

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
        self.list_shortcuts_added = True

        return htmlList

    def _generate_list_skippers(self):
        """
        Generate the list of skippers of page.
        @return: The list of skippers of page.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        container = self.parser.find(
            '#' + self.id_container_skippers
        ).first_result()
        htmlList = None
        if container is None:
            local = self.parser.find('body').first_result()
            if local is not None:
                container = self.parser.create_element('div')
                container.set_attribute('id', self.id_container_skippers)
                local.get_first_element_child().insert_before(container)
        if container is not None:
            htmlList = self.parser.find(container).find_children(
                'ul'
            ).first_result()
            if htmlList is None:
                htmlList = self.parser.create_element('ul')
                container.append_element(htmlList)
        self.list_skippers_added = True

        return htmlList

    def _generate_list_heading(self):
        """
        Generate the list of heading links of page.
        @return: The list of heading links of page.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        container = self.parser.find(
            '#' + self.id_container_heading
        ).first_result()
        htmlList = None
        if container is None:
            local = self.parser.find('body').first_result()
            if local is not None:
                container = self.parser.create_element('div')
                container.set_attribute('id', self.id_container_heading)

                textContainer = self.parser.create_element('span')
                textContainer.set_attribute('id', self.id_text_heading)
                textContainer.append_text(self.text_heading)

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
        self.validate_heading = True
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

    def _generate_anchor_for(self, element, data_attribute, anchor_class):
        """
        Generate an anchor for the element.
        @param element: The element.
        @type element: L{hatemile.util.HTMLDOMElement}
        @param data_attribute: The name of attribute that links the element
        with the anchor.
        @type data_attribute: str
        @param anchor_class: The HTML class of anchor.
        @type anchor_class: str
        @return: The anchor.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        CommonFunctions.generate_id(element, self.prefix_id)
        if self.parser.find(
            '[' + data_attribute + '="' + element.get_attribute('id') + '"]'
        ).first_result() is None:
            if element.get_tag_name() == 'A':
                anchor = element
            else:
                anchor = self.parser.create_element('a')
                CommonFunctions.generate_id(anchor, self.prefix_id)
                anchor.set_attribute('class', anchor_class)
                element.insert_before(anchor)
            if not anchor.has_attribute('name'):
                anchor.set_attribute('name', anchor.get_attribute('id'))
            anchor.set_attribute(data_attribute, element.get_attribute('id'))
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

        if self.list_skippers is not None:
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

        if self.list_shortcuts is not None:
            self.fix_shortcut(element)

    def fix_shortcut(self, element):
        if element.has_attribute('accesskey'):
            description = self._get_description(element)
            if not element.has_attribute('title'):
                element.set_attribute('title', description)

            if not self.list_shortcuts_added:
                self.list_shortcuts = self._generate_list_shortcuts()

            if self.list_shortcuts is not None:
                keys = re.split(
                    '[ \n\t\r]+',
                    element.get_attribute('accesskey')
                )
                for key in keys:
                    key = key.upper()
                    if self.parser.find(self.list_shortcuts).find_children(
                        '[' + self.data_access_key + '="' + key + '"]'
                    ).first_result() is None:
                        item = self.parser.create_element('li')
                        item.set_attribute(self.data_access_key, key)
                        item.append_text(
                            self.prefix
                            + ' + '
                            + key
                            + ': '
                            + description
                        )
                        self.list_shortcuts.append_element(item)

    def fix_shortcuts(self):
        elements = self.parser.find('[accesskey]').list_results()
        for element in elements:
            if not element.has_attribute(self.data_ignore):
                self.fix_shortcut(element)

    def fix_skipper(self, element, skipper):
        if not self.list_skippers_added:
            self.list_skippers = self._generate_list_skippers()
        if self.list_skippers is not None:
            anchor = self._generate_anchor_for(
                element,
                self.data_anchor_for,
                self.class_skipper_anchor
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
                CommonFunctions.generate_id(link, self.prefix_id)

                itemLink.append_element(link)
                self.list_skippers.append_element(itemLink)

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
                if not element.has_attribute(self.data_ignore):
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
        if not self.validate_heading:
            self.valid_heading = self._is_valid_heading()
        if self.valid_heading:
            anchor = self._generate_anchor_for(
                element,
                self.data_heading_anchor_for,
                self.class_heading_anchor
            )
            if anchor is not None:
                listElement = None
                level = self._get_heading_level(element)
                if level == 1:
                    listElement = self._generate_list_heading()
                else:
                    superItem = self.parser.find(
                        '#'
                        + self.id_container_heading
                    ).find_descendants(
                        '['
                        + self.data_heading_level
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
                    item.set_attribute(self.data_heading_level, str(level))

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
            if not element.has_attribute(self.data_ignore):
                self.fix_heading(element)
