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

"""
Module of AccessibleDisplayImplementation class.
"""

import re
from hatemile.accessibledisplay import AccessibleDisplay
from hatemile.util.commonfunctions import CommonFunctions
from hatemile.util.idgenerator import IDGenerator


class AccessibleDisplayImplementation(AccessibleDisplay):
    """
    The AccessibleDisplayImplementation class is official implementation of
    :py:class:`hatemile.accessibledisplay.AccessibleDisplay` for screen
    readers.
    """

    #: The id of list element that contains the description of shortcuts,
    #: before the whole content of page.
    ID_CONTAINER_SHORTCUTS_BEFORE = 'container-shortcuts-before'

    #: The id of list element that contains the description of shortcuts, after
    #: the whole content of page.
    ID_CONTAINER_SHORTCUTS_AFTER = 'container-shortcuts-after'

    #: The HTML class of text of description of container of shortcuts
    #: descriptions.
    CLASS_TEXT_SHORTCUTS = 'text-shortcuts'

    #: The name of attribute that links the description of shortcut of element.
    DATA_ATTRIBUTE_ACCESSKEY_OF = 'data-attributeaccesskeyof'

    def __init__(self, parser, configure, user_agent=None):
        """
        Initializes a new object that manipulate the display for screen readers
        of parser.

        :param parser: The HTML parser.
        :type parser: hatemile.util.html.htmldomparser.HTMLDOMParser
        :param configure: The configuration of HaTeMiLe.
        :type configure: hatemile.util.configure.Configure
        :param user_agent: The user agent of the user.
        :type user_agent: str
        """

        self.parser = parser
        self.id_generator = IDGenerator('display')
        self.shortcut_prefix = self._get_shortcut_prefix(
            user_agent,
            configure.get_parameter('text-standart-shortcut-prefix')
        )
        self.attribute_accesskey_before = configure.get_parameter(
            'attribute-accesskey-before'
        )
        self.attribute_accesskey_after = configure.get_parameter(
            'attribute-accesskey-after'
        )
        self.list_shortcuts_added = False
        self.list_shortcuts_before = None
        self.list_shortcuts_after = None

    def _get_shortcut_prefix(self, user_agent, standart_prefix):
        """
        Returns the shortcut prefix of browser.

        :param user_agent: The user agent of browser.
        :type user_agent: str
        :param standart_prefix: The default prefix.
        :type standart_prefix: str
        :return: The shortcut prefix of browser.
        :rtype: str
        """

        if user_agent is not None:
            user_agent = user_agent.lower()
            opera = 'opera' in user_agent
            mac = 'mac' in user_agent
            konqueror = 'konqueror' in user_agent
            spoofer = 'spoofer' in user_agent
            safari = 'applewebkit' in user_agent
            windows = 'windows' in user_agent
            chrome = 'chrome' in user_agent
            firefox = (
                ('firefox' in user_agent)
                or ('minefield' in user_agent)
            )
            internet_explorer = (
                ('msie' in user_agent)
                or ('trident' in user_agent)
            )

            if opera:
                return 'SHIFT + ESC'
            elif chrome and mac and (not spoofer):
                return 'CTRL + OPTION'
            elif safari and (not windows) and (not spoofer):
                return 'CTRL + ALT'
            elif (not windows) and (safari or mac or konqueror):
                return 'CTRL'
            elif firefox:
                return 'ALT + SHIFT'
            elif chrome or internet_explorer:
                return 'ALT'
            return standart_prefix
        return standart_prefix

    def _get_description(self, element):
        """
        Returns the description of element.

        :param element: The element with description.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :return: The description of element.
        :rtype: str
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
                description_ids = re.split(
                    '[ \n\r\t]+',
                    element.get_attribute('aria-labelledby').strip()
                )
            else:
                description_ids = re.split(
                    '[ \n\r\t]+',
                    element.get_attribute('aria-describedby').strip()
                )
            for description_id in description_ids:
                element_description = self.parser.find(
                    '#' + description_id
                ).first_result()
                if element_description is not None:
                    description = element_description.get_text_content()
                    break
        elif (
            (element.get_tag_name() == 'INPUT')
            and (element.has_attribute('type'))
        ):
            type_attribute = element.get_attribute('type').lower()
            if (
                (
                    (type_attribute == 'button')
                    or (type_attribute == 'submit')
                    or (type_attribute == 'reset')
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
        """

        id_container_shortcuts_before = (
            AccessibleDisplayImplementation.ID_CONTAINER_SHORTCUTS_BEFORE
        )
        id_container_shortcuts_after = (
            AccessibleDisplayImplementation.ID_CONTAINER_SHORTCUTS_AFTER
        )
        local = self.parser.find('body').first_result()
        if local is not None:
            container_before = self.parser.find(
                '#'
                + id_container_shortcuts_before
            ).first_result()
            if (
                (container_before is None)
                and (self.attribute_accesskey_before)
            ):
                container_before = self.parser.create_element('div')
                container_before.set_attribute(
                    'id',
                    id_container_shortcuts_before
                )

                text_container_before = self.parser.create_element('span')
                text_container_before.set_attribute(
                    'class',
                    AccessibleDisplayImplementation.CLASS_TEXT_SHORTCUTS
                )
                text_container_before.append_text(
                    self.attribute_accesskey_before
                )

                container_before.append_element(text_container_before)
                local.prepend_element(container_before)
            if container_before is not None:
                self.list_shortcuts_before = self.parser.find(
                    container_before
                ).find_children('ul').first_result()
                if self.list_shortcuts_before is None:
                    self.list_shortcuts_before = self.parser.create_element(
                        'ul'
                    )
                    container_before.append_element(self.list_shortcuts_before)

            container_after = self.parser.find(
                '#'
                + id_container_shortcuts_after
            ).first_result()
            if (
                (container_after is None)
                and (self.attribute_accesskey_after)
            ):
                container_after = self.parser.create_element('div')
                container_after.set_attribute(
                    'id',
                    id_container_shortcuts_after
                )

                text_container_after = self.parser.create_element('span')
                text_container_after.set_attribute(
                    'class',
                    AccessibleDisplayImplementation.CLASS_TEXT_SHORTCUTS
                )
                text_container_after.append_text(
                    self.attribute_accesskey_after
                )

                container_after.append_element(text_container_after)
                local.append_element(container_after)
            if container_after is not None:
                self.list_shortcuts_after = self.parser.find(
                    container_after
                ).find_children('ul').first_result()
                if self.list_shortcuts_after is None:
                    self.list_shortcuts_after = self.parser.create_element(
                        'ul'
                    )
                    container_after.append_element(self.list_shortcuts_after)
        self.list_shortcuts_added = True

    def display_shortcut(self, element):
        data_attribute_accesskey_of = (
            AccessibleDisplayImplementation.DATA_ATTRIBUTE_ACCESSKEY_OF
        )
        if element.has_attribute('accesskey'):
            description = self._get_description(element)
            if not element.has_attribute('title'):
                element.set_attribute('title', description)

            if not self.list_shortcuts_added:
                self._generate_list_shortcuts()

            keys = re.split(
                '[ \n\t\r]+',
                element.get_attribute('accesskey').upper()
            )
            for key in keys:
                item = self.parser.create_element('li')
                item.set_attribute(data_attribute_accesskey_of, key)
                item.append_text(
                    self.shortcut_prefix
                    + ' + '
                    + key
                    + ': '
                    + description
                )

                selector = (
                    '['
                    + data_attribute_accesskey_of
                    + '="'
                    + key
                    + '"]'
                )
                if (
                    (self.list_shortcuts_before is not None)
                    and (
                        self.parser.find(
                            self.list_shortcuts_before
                        ).find_children(selector).first_result() is None
                    )
                ):
                    self.list_shortcuts_before.append_element(
                        item.clone_element()
                    )
                if (
                    (self.list_shortcuts_after)
                    and (
                        self.parser.find(
                            self.list_shortcuts_after
                        ).find_children(selector).first_result() is None
                    )
                ):
                    self.list_shortcuts_after.append_element(
                        item.clone_element()
                    )

    def display_all_shortcuts(self):
        elements = self.parser.find('[accesskey]').list_results()
        for element in elements:
            if CommonFunctions.is_valid_element(element):
                self.display_shortcut(element)
