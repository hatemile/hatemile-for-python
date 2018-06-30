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
Module of AccessibleNavigationImplementation class.
"""

import os
import re
from xml.dom import minidom
from hatemile import helper
from hatemile.accessiblenavigation import AccessibleNavigation
from hatemile.util.commonfunctions import CommonFunctions
from hatemile.util.configure import Configure
from hatemile.util.idgenerator import IDGenerator
from hatemile.util.html.htmldomparser import HTMLDOMParser


class AccessibleNavigationImplementation(AccessibleNavigation):
    """
    The AccessibleNavigationImplementation class is official implementation of
    :py:class:`hatemile.accessiblenavigation.AccessibleNavigation`.
    """

    #: The id of list element that contains the skippers.
    ID_CONTAINER_SKIPPERS = 'container-skippers'

    #: The id of list element that contains the links for the headings, before
    #: the whole content of page.
    ID_CONTAINER_HEADING_BEFORE = 'container-heading-before'

    #: The id of list element that contains the links for the headings, after
    #: the whole content of page.
    ID_CONTAINER_HEADING_AFTER = 'container-heading-after'

    #: The HTML class of text of description of container of heading links.
    CLASS_TEXT_HEADING = 'text-heading'

    #: The HTML class of anchor of skipper.
    CLASS_SKIPPER_ANCHOR = 'skipper-anchor'

    #: The HTML class of anchor of heading link.
    CLASS_HEADING_ANCHOR = 'heading-anchor'

    #: The HTML class of force link, before it.
    CLASS_FORCE_LINK_BEFORE = 'force-link-before'

    #: The HTML class of force link, after it.
    CLASS_FORCE_LINK_AFTER = 'force-link-after'

    #: The name of attribute that links the anchor of skipper with the element.
    DATA_ANCHOR_FOR = 'data-anchorfor'

    #: The name of attribute that indicates the level of heading of link.
    DATA_HEADING_LEVEL = 'data-headinglevel'

    #: The name of attribute that links the anchor of heading link with
    #: heading.
    DATA_HEADING_ANCHOR_FOR = 'data-headinganchorfor'

    #: The name of attribute that link the anchor of long description with the
    #: image.
    DATA_ATTRIBUTE_LONG_DESCRIPTION_OF = 'data-attributelongdescriptionof'

    def __init__(
        self,
        parser,
        configure,
        skipper_file_name=None
    ):
        """
        Initializes a new object that manipulate the accessibility of the
        navigation of parser.

        :param parser: The HTML parser.
        :type parser: hatemile.util.html.htmldomparser.HTMLDOMParser
        :param configure: The configuration of HaTeMiLe.
        :type configure: hatemile.util.configure.Configure
        :param skipper_file_name: The file path of skippers configuration.
        :type skipper_file_name: str
        """

        helper.require_not_none(parser, configure)
        helper.require_valid_type(parser, HTMLDOMParser)
        helper.require_valid_type(configure, Configure)
        helper.require_valid_type(skipper_file_name, str)

        self.parser = parser
        self.id_generator = IDGenerator('navigation')
        self.elements_heading_before = configure.get_parameter(
            'elements-heading-before'
        )
        self.elements_heading_after = configure.get_parameter(
            'elements-heading-after'
        )
        self.attribute_long_description_prefix_before = (
            configure.get_parameter(
                'attribute-longdescription-prefix-before'
            )
        )
        self.attribute_long_description_suffix_before = (
            configure.get_parameter(
                'attribute-longdescription-suffix-before'
            )
        )
        self.attribute_long_description_prefix_after = configure.get_parameter(
            'attribute-longdescription-prefix-after'
        )
        self.attribute_long_description_suffix_after = configure.get_parameter(
            'attribute-longdescription-suffix-after'
        )
        self.skippers = AccessibleNavigationImplementation._get_skippers(
            configure,
            skipper_file_name
        )
        self.list_skippers_added = False
        self.list_heading_added = False
        self.validate_heading = False
        self.valid_heading = False
        self.list_skippers = None
        self.list_heading_before = None
        self.list_heading_after = None

    @staticmethod
    def _get_skippers(configure, file_name=None):
        """
        Returns the skippers of configuration.

        :param configure: The configuration of HaTeMiLe.
        :type configure: hatemile.util.configure.Configure
        :param file_name: The file path of skippers configuration.
        :type file_name: str
        :return: The skippers of configuration.
        :rtype: list(dict(str, str))
        """

        skippers = []
        if file_name is None:
            file_name = os.path.join(os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.realpath(__file__))
            )), 'skippers.xml')
        xmldoc = minidom.parse(file_name)
        skippers_xml = xmldoc.getElementsByTagName(
            'skippers'
        )[0].getElementsByTagName('skipper')
        for skipper_xml in skippers_xml:
            skippers.append({
                'selector': skipper_xml.attributes['selector'].value,
                'description': configure.get_parameter(
                    skipper_xml.attributes['description'].value
                ),
                'shortcut': skipper_xml.attributes['shortcut'].value
            })
        return skippers

    def _generate_list_skippers(self):
        """
        Generate the list of skippers of page.

        :return: The list of skippers of page.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        container = self.parser.find(
            '#'
            + AccessibleNavigationImplementation.ID_CONTAINER_SKIPPERS
        ).first_result()
        html_list = None
        if container is None:
            local = self.parser.find('body').first_result()
            if local is not None:
                container = self.parser.create_element('div')
                container.set_attribute(
                    'id',
                    AccessibleNavigationImplementation.ID_CONTAINER_SKIPPERS
                )
                local.prepend_element(container)
        if container is not None:
            html_list = self.parser.find(container).find_children(
                'ul'
            ).first_result()
            if html_list is None:
                html_list = self.parser.create_element('ul')
                container.append_element(html_list)
        self.list_skippers_added = True

        return html_list

    def _generate_list_heading(self):
        """
        Generate the list of heading links of page.
        """

        local = self.parser.find('body').first_result()
        id_container_heading_before = (
            AccessibleNavigationImplementation.ID_CONTAINER_HEADING_BEFORE
        )
        id_container_heading_after = (
            AccessibleNavigationImplementation.ID_CONTAINER_HEADING_AFTER
        )
        if local is not None:
            container_before = self.parser.find(
                '#'
                + id_container_heading_before
            ).first_result()
            if (container_before is None) and (self.elements_heading_before):
                container_before = self.parser.create_element('div')
                container_before.set_attribute(
                    'id',
                    id_container_heading_before
                )

                text_container_before = self.parser.create_element('span')
                text_container_before.set_attribute(
                    'class',
                    AccessibleNavigationImplementation.CLASS_TEXT_HEADING
                )
                text_container_before.append_text(self.elements_heading_before)

                container_before.append_element(text_container_before)
                local.prepend_element(container_before)
            if container_before is not None:
                self.list_heading_before = self.parser.find(
                    container_before
                ).find_children('ol').first_result()
                if self.list_heading_before is None:
                    self.list_heading_before = self.parser.create_element('ol')
                    container_before.append_element(self.list_heading_before)

            container_after = self.parser.find(
                '#'
                + id_container_heading_after
            ).first_result()
            if (container_after is None) and (self.elements_heading_after):
                container_after = self.parser.create_element('div')
                container_after.set_attribute('id', id_container_heading_after)

                text_container_after = self.parser.create_element('span')
                text_container_after.set_attribute(
                    'class',
                    AccessibleNavigationImplementation.CLASS_TEXT_HEADING
                )
                text_container_after.append_text(self.elements_heading_after)

                container_after.append_element(text_container_after)
                local.append_element(container_after)
            if container_after is not None:
                self.list_heading_after = self.parser.find(
                    container_after
                ).find_children('ol').first_result()
                if self.list_heading_after is None:
                    self.list_heading_after = self.parser.create_element('ol')
                    container_after.append_element(self.list_heading_after)
        self.list_heading_added = True

    def _get_heading_level(self, element):
        """
        Returns the level of heading.

        :param element: The heading.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :return: The level of heading.
        :rtype: int
        """
        # pylint: disable=no-self-use

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
        return -1

    def _is_valid_heading(self):
        """
        Check that the headings of page are sintatic correct.

        :return: True if the headings of page are sintatic correct or False if
                 not.
        :rtype: bool
        """

        elements = self.parser.find('h1,h2,h3,h4,h5,h6').list_results()
        last_level = 0
        count_main_heading = 0
        self.validate_heading = True
        for element in elements:
            level = self._get_heading_level(element)
            if level == 1:
                if count_main_heading == 1:
                    return False
                else:
                    count_main_heading = 1
            if (level - last_level) > 1:
                return False
            last_level = level
        return True

    def _generate_anchor_for(self, element, data_attribute, anchor_class):
        """
        Generate an anchor for the element.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :param data_attribute: The name of attribute that links the element
                               with the anchor.
        :type data_attribute: str
        :param anchor_class: The HTML class of anchor.
        :type anchor_class: str
        :return: The anchor.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        self.id_generator.generate_id(element)
        if self.parser.find(
            '[' + data_attribute + '="' + element.get_attribute('id') + '"]'
        ).first_result() is None:
            if element.get_tag_name() == 'A':
                anchor = element
            else:
                anchor = self.parser.create_element('a')
                self.id_generator.generate_id(anchor)
                anchor.set_attribute('class', anchor_class)
                element.insert_before(anchor)
            if not anchor.has_attribute('name'):
                anchor.set_attribute('name', anchor.get_attribute('id'))
            anchor.set_attribute(data_attribute, element.get_attribute('id'))
            return anchor
        return None

    def _free_shortcut(self, shortcut):
        """
        Replace the shortcut of elements, that has the shortcut passed.

        :param shortcut: The shortcut.
        :type shortcut: str
        """

        alpha_numbers = '1234567890abcdefghijklmnopqrstuvwxyz'
        elements = self.parser.find('[accesskey]').list_results()
        found = False
        for element in elements:
            shortcuts = element.get_attribute('accesskey').lower()
            if CommonFunctions.in_list(shortcuts, shortcut):
                for key in alpha_numbers:
                    found = True
                    for element_with_shortcuts in elements:
                        shortcuts = element_with_shortcuts.get_attribute(
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

    def provide_navigation_by_skipper(self, element):
        if not self.list_skippers_added:
            self.list_skippers = self._generate_list_skippers()
        if self.list_skippers is not None:
            skipper = None
            for auxiliar_skipper in self.skippers:
                elements = self.parser.find(
                    auxiliar_skipper['selector']
                ).list_results()
                if element in elements:
                    skipper = auxiliar_skipper
                    break
            if skipper is not None:
                anchor = self._generate_anchor_for(
                    element,
                    AccessibleNavigationImplementation.DATA_ANCHOR_FOR,
                    AccessibleNavigationImplementation.CLASS_SKIPPER_ANCHOR
                )
                if anchor is not None:
                    item_link = self.parser.create_element('li')
                    link = self.parser.create_element('a')
                    link.set_attribute(
                        'href',
                        '#' + anchor.get_attribute('name')
                    )
                    link.append_text(skipper['description'])

                    shortcuts = skipper['shortcut']
                    if shortcuts:
                        shortcut = shortcuts[0]
                        if shortcut != '':
                            self._free_shortcut(shortcut)
                            link.set_attribute('accesskey', shortcut)
                    self.id_generator.generate_id(link)

                    item_link.append_element(link)
                    self.list_skippers.append_element(item_link)

    def provide_navigation_by_all_skippers(self):
        for skipper in self.skippers:
            elements = self.parser.find(skipper['selector']).list_results()
            for element in elements:
                if CommonFunctions.is_valid_element(element):
                    self.provide_navigation_by_skipper(element)

    def provide_navigation_by_heading(self, heading):
        if not self.validate_heading:
            self.valid_heading = self._is_valid_heading()
        if self.valid_heading:
            anchor = self._generate_anchor_for(
                heading,
                AccessibleNavigationImplementation.DATA_HEADING_ANCHOR_FOR,
                AccessibleNavigationImplementation.CLASS_HEADING_ANCHOR
            )
            if anchor is not None:
                if not self.list_heading_added:
                    self._generate_list_heading()
                list_before = None
                list_after = None
                level = self._get_heading_level(heading)
                if level == 1:
                    list_before = self.list_heading_before
                    list_after = self.list_heading_after
                else:
                    selector = (
                        '['
                        + AccessibleNavigationImplementation.DATA_HEADING_LEVEL
                        + '="'
                        + str(level - 1)
                        + '"]'
                    )
                    if self.list_heading_before is not None:
                        super_item_before = self.parser.find(
                            self.list_heading_before
                        ).find_descendants(selector).last_result()
                        if super_item_before is not None:
                            list_before = self.parser.find(
                                super_item_before
                            ).find_children('ol').first_result()
                            if list_before is None:
                                list_before = self.parser.create_element('ol')
                                super_item_before.append_element(list_before)
                    if self.list_heading_after is not None:
                        super_item_after = self.parser.find(
                            self.list_heading_after
                        ).find_descendants(selector).last_result()
                        if super_item_after is not None:
                            list_after = self.parser.find(
                                super_item_after
                            ).find_children('ol').first_result()
                            if list_after is None:
                                list_after = self.parser.create_element('ol')
                                super_item_after.append_element(list_after)
                item = self.parser.create_element('li')
                item.set_attribute(
                    AccessibleNavigationImplementation.DATA_HEADING_LEVEL,
                    str(level)
                )

                link = self.parser.create_element('a')
                link.set_attribute(
                    'href',
                    '#' + anchor.get_attribute('name')
                )
                link.append_text(heading.get_text_content())
                item.append_element(link)

                if list_before is not None:
                    list_before.append_element(item.clone_element())
                if list_after is not None:
                    list_after.append_element(item.clone_element())

    def provide_navigation_by_all_headings(self):
        headings = self.parser.find('h1,h2,h3,h4,h5,h6').list_results()
        for heading in headings:
            if CommonFunctions.is_valid_element(heading):
                self.provide_navigation_by_heading(heading)

    def provide_navigation_to_long_description(self, image):
        custom_attribute = (
            AccessibleNavigationImplementation
            .DATA_ATTRIBUTE_LONG_DESCRIPTION_OF
        )
        if (image.has_attribute('longdesc')) and (image.has_attribute('alt')):
            self.id_generator.generate_id(image)
            id_image = image.get_attribute('id')
            selector = (
                '['
                + custom_attribute
                + '="'
                + id_image
                + '"]'
            )
            selector_before = (
                '.'
                + AccessibleNavigationImplementation.CLASS_FORCE_LINK_BEFORE
                + selector
            )
            selector_after = (
                '.'
                + AccessibleNavigationImplementation.CLASS_FORCE_LINK_AFTER
                + selector
            )
            if (
                (self.attribute_long_description_prefix_before)
                and (self.attribute_long_description_suffix_before)
                and (self.parser.find(selector_before).first_result() is None)
            ):
                before_text = (
                    self.attribute_long_description_prefix_before
                    + re.sub(
                        '[ \n\r\t]+',
                        ' ',
                        image.get_attribute('alt').strip()
                    )
                    + self.attribute_long_description_suffix_before
                ).strip()
                before_anchor = self.parser.create_element('a')
                before_anchor.set_attribute(
                    'href',
                    image.get_attribute('longdesc')
                )
                before_anchor.set_attribute('target', '_blank')
                before_anchor.set_attribute(custom_attribute, id_image)
                before_anchor.set_attribute(
                    'class',
                    AccessibleNavigationImplementation.CLASS_FORCE_LINK_BEFORE
                )
                before_anchor.append_text(before_text)
                image.insert_after(before_anchor)
            if (
                (self.attribute_long_description_prefix_after)
                and (self.attribute_long_description_suffix_after)
                and (self.parser.find(selector_after).first_result() is None)
            ):
                after_text = (
                    self.attribute_long_description_prefix_after
                    + re.sub(
                        '[ \n\r\t]+',
                        ' ',
                        image.get_attribute('alt').strip()
                    )
                    + self.attribute_long_description_suffix_after
                ).strip()
                after_anchor = self.parser.create_element('a')
                after_anchor.set_attribute(
                    'href',
                    image.get_attribute('longdesc')
                )
                after_anchor.set_attribute('target', '_blank')
                after_anchor.set_attribute(custom_attribute, id_image)
                after_anchor.set_attribute(
                    'class',
                    AccessibleNavigationImplementation.CLASS_FORCE_LINK_AFTER
                )
                after_anchor.append_text(after_text)
                image.insert_after(after_anchor)

    def provide_navigation_to_all_long_descriptions(self):
        images = self.parser.find('[longdesc]').list_results()
        for image in images:
            if CommonFunctions.is_valid_element(image):
                self.provide_navigation_to_long_description(image)
