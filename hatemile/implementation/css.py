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
Module of AccessibleCSSImplementation class.
"""

import os
import re
from xml.dom import minidom
from hatemile import helper
from hatemile.accessiblecss import AccessibleCSS
from hatemile.util.commonfunctions import CommonFunctions
from hatemile.util.configure import Configure
from hatemile.util.css.stylesheetparser import StyleSheetParser
from hatemile.util.html.htmldomparser import HTMLDOMParser
from hatemile.util.html.htmldomtextnode import HTMLDOMTextNode
from .display import AccessibleDisplayImplementation


class AccessibleCSSImplementation(AccessibleCSS):
    """
    The AccessibleCSSImplementation class is official implementation of
    :py:class:`hatemile.accessiblecss.AccessibleCSS`.
    """

    #: The name of attribute for identify isolator elements.
    DATA_ISOLATOR_ELEMENT = 'data-auxiliarspan'

    #: The name of attribute for identify the element created or modified to
    #: support speak property.
    DATA_SPEAK = 'data-cssspeak'

    #: The name of attribute for identify the element created or modified to
    #: support speak-as property.
    DATA_SPEAK_AS = 'data-cssspeakas'

    #: The valid element tags for inherit the speak and speak-as properties.
    VALID_INHERIT_TAGS = [
        'SPAN',
        'A',
        'RT',
        'DFN',
        'ABBR',
        'Q',
        'CITE',
        'EM',
        'TIME',
        'VAR',
        'SAMP',
        'I',
        'B',
        'SUB',
        'SUP',
        'SMALL',
        'STRONG',
        'MARK',
        'RUBY',
        'INS',
        'DEL',
        'KBD',
        'BDO',
        'CODE',
        'P',
        'FIGCAPTION',
        'FIGURE',
        'PRE',
        'DIV',
        'OL',
        'UL',
        'LI',
        'BLOCKQUOTE',
        'DL',
        'DT',
        'DD',
        'FIELDSET',
        'LEGEND',
        'LABEL',
        'FORM',
        'BODY',
        'ASIDE',
        'ADDRESS',
        'H1',
        'H2',
        'H3',
        'H4',
        'H5',
        'H6',
        'SECTION',
        'HEADER',
        'NAV',
        'ARTICLE',
        'FOOTER',
        'HGROUP',
        'CAPTION',
        'SUMMARY',
        'DETAILS',
        'TABLE',
        'TR',
        'TD',
        'TH',
        'TBODY',
        'THEAD',
        'TFOOT'
    ]

    #: The valid element tags for speak and speak-as properties.
    VALID_TAGS = [
        'SPAN',
        'A',
        'RT',
        'DFN',
        'ABBR',
        'Q',
        'CITE',
        'EM',
        'TIME',
        'VAR',
        'SAMP',
        'I',
        'B',
        'SUB',
        'SUP',
        'SMALL',
        'STRONG',
        'MARK',
        'RUBY',
        'INS',
        'DEL',
        'KBD',
        'BDO',
        'CODE',
        'P',
        'FIGCAPTION',
        'FIGURE',
        'PRE',
        'DIV',
        'LI',
        'BLOCKQUOTE',
        'DT',
        'DD',
        'FIELDSET',
        'LEGEND',
        'LABEL',
        'FORM',
        'BODY',
        'ASIDE',
        'ADDRESS',
        'H1',
        'H2',
        'H3',
        'H4',
        'H5',
        'H6',
        'SECTION',
        'HEADER',
        'NAV',
        'ARTICLE',
        'FOOTER',
        'CAPTION',
        'SUMMARY',
        'DETAILS',
        'TD',
        'TH'
    ]

    def __init__(
        self,
        html_parser,
        css_parser,
        configure,
        symbol_file_name=None
    ):
        """
        Initializes a new object that manipulate the accessibility of the CSS
        of parser.

        :param html_parser: The HTML parser.
        :type html_parser: hatemile.util.html.htmldomparser.HTMLDOMParser
        :param css_parser: The CSS parser.
        :type css_parser: hatemile.util.css.stylesheetparser.StyleSheetParser
        :param configure: The configuration of HaTeMiLe.
        :type configure: hatemile.util.configure.Configure
        :param symbol_file_name: The file path of symbol configuration.
        :type symbol_file_name: str
        """

        helper.require_not_none(html_parser, css_parser, configure)
        helper.require_valid_type(html_parser, HTMLDOMParser)
        helper.require_valid_type(css_parser, StyleSheetParser)
        helper.require_valid_type(configure, Configure)
        helper.require_valid_type(symbol_file_name, str)

        self.html_parser = html_parser
        self.css_parser = css_parser
        self.configure = configure
        self._set_symbols(symbol_file_name, configure)

    def _operation_speak_as_spell_out(self, content, index, children):
        """
        The operation method of _speak_as method for spell-out.

        :param content: The text content of element.
        :type content: str
        :param index: The index of pattern in text content of element.
        :type index: int
        :param children: The children of element.
        :type children: list(hatemile.util.html.htmldomelement.HTMLDOMElement)
        """

        children.append(self._create_content_element(
            content[0:(index + 1)],
            'spell-out'
        ))

        children.append(self._create_aural_content_element(' ', 'spell-out'))

        return children

    def _operation_speak_as_literal_punctuation(
        self,
        content,
        index,
        children
    ):
        """
        The operation method of _speak_as method for literal-punctuation.

        :param content: The text content of element.
        :type content: str
        :param index: The index of pattern in text content of element.
        :type index: int
        :param children: The children of element.
        :type children: list(hatemile.util.html.htmldomelement.HTMLDOMElement)
        """

        data_property_value = 'literal-punctuation'
        if index != 0:
            children.append(self._create_content_element(
                content[0:index],
                data_property_value
            ))
        children.append(self._create_aural_content_element(
            (
                ' '
                + self._get_description_of_symbol(content[index:(index + 1)])
                + ' '
            ),
            data_property_value)
        )

        children.append(self._create_visual_content_element(
            content[index:(index + 1)],
            data_property_value
        ))

        return children

    def _operation_speak_as_no_punctuation(self, content, index, children):
        """
        The operation method of _speak_as method for no-punctuation.

        :param content: The text content of element.
        :type content: str
        :param index: The index of pattern in text content of element.
        :type index: int
        :param children: The children of element.
        :type children: list(hatemile.util.html.htmldomelement.HTMLDOMElement)
        """

        if index != 0:
            children.append(self._create_content_element(
                content[0:index],
                'no-punctuation'
            ))
        children.append(self._create_visual_content_element(
            content[index:(index + 1)],
            'no-punctuation'
        ))

        return children

    def _operation_speak_as_digits(self, content, index, children):
        """
        The operation method of _speak_as method for digits.

        :param content: The text content of element.
        :type content: str
        :param index: The index of pattern in text content of element.
        :type index: int
        :param children: The children of element.
        :type children: list(hatemile.util.html.htmldomelement.HTMLDOMElement)
        """

        data_property_value = 'digits'
        if index != 0:
            children.append(self._create_content_element(
                content[0:index],
                data_property_value
            ))
        children.append(self._create_aural_content_element(
            ' ',
            data_property_value
        ))

        children.append(self._create_content_element(
            content[index:(index + 1)],
            data_property_value
        ))

        return children

    def _set_symbols(self, file_name, configure):
        """
        Load the symbols with configuration.

        :param file_name: The file path of symbol configuration.
        :type file_name: str
        :param configure: The configuration of HaTeMiLe.
        :type configure: hatemile.util.configure.Configure
        """

        self.symbols = []
        if file_name is None:
            file_name = os.path.join(os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.realpath(__file__))
            )), 'symbols.xml')
        xmldoc = minidom.parse(file_name)
        symbols_xml = xmldoc.getElementsByTagName(
            'symbols'
        )[0].getElementsByTagName('symbol')
        for symbol_xml in symbols_xml:
            self.symbols.append({
                'symbol': symbol_xml.attributes['symbol'].value,
                'description': configure.get_parameter(
                    symbol_xml.attributes['description'].value
                )
            })

    def _get_formated_symbol(self, symbol):
        """
        Returns the symbol formated to be searched by regular expression.

        :param symbol: The symbol.
        :type symbol: str
        :return: The symbol formated.
        :rtype: str
        """
        # pylint: disable=no-self-use

        old_symbols = [
            '\\',
            '.',
            '+',
            '*',
            '?',
            '^',
            '$',
            '[',
            ']',
            '{',
            '}',
            '(',
            ')',
            '|',
            '/',
            ',',
            '!',
            '=',
            ':',
            '-'
        ]
        replace_dict = {
            '\\': '\\\\',
            '.': r'\.',
            '+': r'\+',
            '*': r'\*',
            '?': r'\?',
            '^': r'\^',
            '$': r'\$',
            '[': r'\[',
            ']': r'\]',
            '{': r'\{',
            '}': r'\}',
            '(': r'\(',
            ')': r'\)',
            '|': r'\|',
            '/': r'\/',
            ',': r'\,',
            '!': r'\!',
            '=': r'\=',
            ':': r'\:',
            '-': r'\-'
        }
        for old in old_symbols:
            symbol = symbol.replace(old, replace_dict[old])
        return symbol

    def _get_description_of_symbol(self, symbol):
        """
        Returns the description of symbol.

        :param symbol: The symbol.
        :type symbol: str
        :return: The description of symbol.
        :rtype: str
        """

        for dict_symbol in self.symbols:
            if dict_symbol['symbol'] == symbol:
                return dict_symbol['description']
        return None

    def _get_regular_expression_of_symbols(self):
        """
        Returns the regular expression to search all symbols.

        :return: The regular expression to search all symbols.
        :rtype: str
        """

        regular_expression = None
        for symbol in self.symbols:
            formated_symbol = self._get_formated_symbol(symbol['symbol'])
            if regular_expression is None:
                regular_expression = '(' + formated_symbol + ')'
            else:
                regular_expression = (
                    regular_expression +
                    '|(' +
                    formated_symbol +
                    ')'
                )
        return regular_expression

    def _is_valid_inherit_element(self, element):
        """
        Check that the children of element can be manipulated to apply the CSS
        properties.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :return: True if the children of element can be manipulated to apply
                 the CSS properties or False if the children of element cannot
                 be manipulated to apply the CSS properties.
        :rtype: bool
        """
        # pylint: disable=no-self-use

        tag_name = element.get_tag_name()
        return (
            (tag_name in AccessibleCSSImplementation.VALID_INHERIT_TAGS)
            and (not element.has_attribute(CommonFunctions.DATA_IGNORE))
        )

    def _is_valid_element(self, element):
        """
        Check that the element can be manipulated to apply the CSS properties.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :return: True if the element can be manipulated to apply the CSS
                 properties or False if the element cannot be manipulated to
                 apply the CSS properties.
        :rtype: bool
        """
        # pylint: disable=no-self-use

        return element.get_tag_name() in AccessibleCSSImplementation.VALID_TAGS

    def _isolate_text_node(self, element):
        """
        Isolate text nodes of element nodes.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        if (
            (element.has_children_elements())
            and (self._is_valid_element(element))
        ):
            if self._is_valid_element(element):
                child_nodes = element.get_children()
                for child_node in child_nodes:
                    if isinstance(child_node, HTMLDOMTextNode):
                        span = self.html_parser.create_element('span')
                        span.set_attribute(
                            AccessibleCSSImplementation.DATA_ISOLATOR_ELEMENT,
                            'true'
                        )
                        span.append_text(child_node.get_text_content())

                        child_node.replace_node(span)
            children = element.get_children_elements()
            for child in children:
                self._isolate_text_node(child)

    def _replace_element_by_own_content(self, element):
        """
        Replace the element by own text content.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """
        # pylint: disable=no-self-use

        if element.has_children_elements():
            children = element.get_children_elements()
            for child in children:
                element.insert_before(child)
            element.remove_node()
        elif element.has_children():
            element.replace_node(element.get_first_node_child())

    def _visit(self, element, operation):
        """
        Visit and execute a operation in element and descendants.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :param operation: The operation to be executed.
        :type operation: function
        """

        if self._is_valid_inherit_element(element):
            if element.has_children_elements():
                children = element.get_children_elements()
                for child in children:
                    self._visit(child, operation)
            elif self._is_valid_element(element):
                operation(element)

    def _create_content_element(self, content, data_property_value):
        """
        Create a element to show the content.

        :param content: The text content of element.
        :type content: str
        :param data_property_value: The value of custom attribute used to
                                    identify the fix.
        :type data_property_value: str
        :return: The element to show the content.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        content_element = self.html_parser.create_element('span')
        content_element.set_attribute(
            AccessibleCSSImplementation.DATA_ISOLATOR_ELEMENT,
            'true'
        )
        content_element.set_attribute(
            AccessibleCSSImplementation.DATA_SPEAK_AS,
            data_property_value
        )
        content_element.append_text(content)
        return content_element

    def _create_aural_content_element(self, content, data_property_value):
        """
        Create a element to show the content, only to aural displays.

        :param content: The text content of element.
        :type content: str
        :param data_property_value: The value of custom attribute used to
                                    identify the fix.
        :type data_property_value: str
        :return: The element to show the content.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        content_element = self._create_content_element(
            content,
            data_property_value
        )
        content_element.set_attribute('unselectable', 'on')
        content_element.set_attribute('class', 'screen-reader-only')
        return content_element

    def _create_visual_content_element(self, content, data_property_value):
        """
        Create a element to show the content, only to visual displays.

        :param content: The text content of element.
        :type content: str
        :param data_property_value: The value of custom attribute used to
                                    identify the fix.
        :type data_property_value: str
        :return: The element to show the content.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        content_element = self._create_content_element(
            content,
            data_property_value
        )
        content_element.set_attribute('aria-hidden', 'true')
        content_element.set_attribute('role', 'presentation')
        return content_element

    def _speak_normal(self, element):
        """
        Speak the content of element only.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        if element.has_attribute(AccessibleCSSImplementation.DATA_SPEAK):
            if (
                (element.get_attribute(
                    AccessibleCSSImplementation.DATA_SPEAK
                ) == 'none')
                and (not element.has_attribute(
                    AccessibleCSSImplementation.DATA_ISOLATOR_ELEMENT
                ))
            ):
                element.remove_attribute('role')
                element.remove_attribute('aria-hidden')
                element.remove_attribute(
                    AccessibleCSSImplementation.DATA_SPEAK
                )
            else:
                self._replace_element_by_own_content(element)

    def _speak_normal_inherit(self, element):
        """
        Speak the content of element and descendants.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        self._visit(element, self._speak_normal)

        element.normalize()

    def _speak_none(self, element):
        """
        No speak any content of element only.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """
        # pylint: disable=no-self-use

        element.set_attribute('role', 'presentation')
        element.set_attribute('aria-hidden', 'true')
        element.set_attribute(AccessibleCSSImplementation.DATA_SPEAK, 'none')

    def _speak_none_inherit(self, element):
        """
        No speak any content of element and descendants.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        self._isolate_text_node(element)

        self._visit(element, self._speak_none)

    def _speak_as(
        self,
        element,
        regular_expression,
        data_property_value,
        operation
    ):
        """
        Execute a operation by regular expression for element only.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :param regular_expression: The regular expression.
        :type regular_expression: str
        :param data_property_value: The value of custom attribute used to
                                    identify the fix.
        :type data_property_value: str
        :param operation: The operation to be executed.
        :type operation: function
        """

        children = []
        pattern = re.compile(regular_expression)
        content = element.get_text_content()
        while content:
            matches = pattern.search(content)
            if matches is not None:
                index = matches.start()
                children = operation(content, index, children)

                new_index = index + 1
                content = content[new_index:]
            else:
                break
        if children:
            if content:
                children.append(self._create_content_element(
                    content,
                    data_property_value
                ))
            while element.has_children():
                element.get_first_node_child().remove_node()
            for child in children:
                element.append_element(child)

    def _reverse_speak_as(self, element, data_property_value):
        """
        Revert changes of a speak_as method for element and descendants.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :param data_property_value: The value of custom attribute used to
                                    identify the fix.
        :type data_property_value: str
        """

        data_property = (
            '['
            + AccessibleCSSImplementation.DATA_SPEAK_AS
            + '="'
            + data_property_value
            + '"]'
        )

        auxiliar_elements = self.html_parser.find(element).find_descendants(
            data_property
        ).list_results()
        for auxiliar_element in auxiliar_elements:
            auxiliar_element.remove_node()

        content_elements = self.html_parser.find(element).find_descendants(
            data_property
        ).list_results()
        for content_element in content_elements:
            if (
                (element.has_attribute(
                    AccessibleCSSImplementation.DATA_ISOLATOR_ELEMENT
                ))
                and (element.has_attribute(
                    AccessibleCSSImplementation.DATA_ISOLATOR_ELEMENT
                ) == 'true')
            ):
                self._replace_element_by_own_content(content_element)

        element.normalize()

    def _speak_as_normal(self, element):
        """
        Use the default speak configuration of user agent for element and
        descendants.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        self._reverse_speak_as(element, 'spell-out')
        self._reverse_speak_as(element, 'literal-punctuation')
        self._reverse_speak_as(element, 'no-punctuation')
        self._reverse_speak_as(element, 'digits')

    def _speak_as_spell_out(self, element):
        """
        Speak one letter at a time for each word for element only.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        self._speak_as(
            element,
            '[a-zA-Z]',
            'spell-out',
            self._operation_speak_as_spell_out
        )

    def _speak_as_spell_out_inherit(self, element):
        """
        Speak one letter at a time for each word for elements and descendants.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        self._reverse_speak_as(element, 'spell-out')

        self._isolate_text_node(element)

        self._visit(element, self._speak_as_spell_out)

    def _speak_as_literal_punctuation(self, element):
        """
        Speak the punctuation for elements only.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        self._speak_as(
            element,
            self._get_regular_expression_of_symbols(),
            'literal-punctuation',
            self._operation_speak_as_literal_punctuation
        )

    def _speak_as_literal_punctuation_inherit(self, element):
        """
        Speak the punctuation for elements and descendants.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        self._reverse_speak_as(element, 'literal-punctuation')
        self._reverse_speak_as(element, 'no-punctuation')

        self._isolate_text_node(element)

        self._visit(element, self._speak_as_literal_punctuation)

    def _speak_as_no_punctuation(self, element):
        """
        No speak the punctuation for element only.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        self._speak_as(
            element,
            (
                '[!"#$%&\'\\(\\)\\*\\+,-\\.\\/:;<=>?@\\[\\\\\\]\\^_`\\'
                + '{\\|\\}\\~]'
            ),
            'no-punctuation',
            self._operation_speak_as_no_punctuation
        )

    def _speak_as_no_punctuation_inherit(self, element):
        """
        No speak the punctuation for element and descendants.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        self._reverse_speak_as(element, 'literal-punctuation')
        self._reverse_speak_as(element, 'no-punctuation')

        self._isolate_text_node(element)

        self._visit(element, self._speak_as_no_punctuation)

    def _speak_as_digits(self, element):
        """
        Speak the digit at a time for each number for element only.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        self._speak_as(
            element,
            '[0-9]',
            'digits',
            self._operation_speak_as_digits
        )

    def _speak_as_digits_inherit(self, element):
        """
        Speak the digit at a time for each number for element and descendants.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        self._reverse_speak_as(element, 'digits')

        self._isolate_text_node(element)

        self._visit(element, self._speak_as_digits)

    def _speak_as_continuous_inherit(self, element):
        """
        Speaks the numbers for element and descendants as a word number.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        self._reverse_speak_as(element, 'digits')

    def _speak_header_always_inherit(self, element):
        """
        The cells headers will be spoken for every data cell for element and
        descendants.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        self._speak_header_once_inherit(element)

        cell_elements = self.html_parser.find(element).find_descendants(
            'td[headers],th[headers]'
        ).list_results()
        accessible_display = AccessibleDisplayImplementation(
            self.html_parser,
            self.configure
        )
        for cell_element in cell_elements:
            accessible_display.display_cell_header(cell_element)

    def _speak_header_once_inherit(self, element):
        """
        The cells headers will be spoken one time for element and descendants.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        header_elements = self.html_parser.find(element).find_descendants(
            '['
            + AccessibleDisplayImplementation.DATA_ATTRIBUTE_HEADERS_OF
            + ']'
        ).list_results()
        for header_element in header_elements:
            header_element.remove_node()

    def _provide_speak_properties_with_rule(self, element, rule):
        """
        Provide the CSS features of speaking and speech properties in element.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :param rule: The stylesheet rule.
        :type rule: hatemile.util.css.stylesheetrule.StyleSheetRule
        """

        if rule.has_property('speak'):
            declarations = rule.get_declarations('speak')
            for declaration in declarations:
                property_value = declaration.get_value()
                if property_value == 'none':
                    self._speak_none_inherit(element)
                elif property_value == 'normal':
                    self._speak_normal_inherit(element)
                elif property_value == 'spell-out':
                    self._speak_as_spell_out_inherit(element)
        if rule.has_property('speak-as'):
            declarations = rule.get_declarations('speak-as')
            for declaration in declarations:
                speak_as_values = declaration.get_values()
                self._speak_as_normal(element)
                for speak_as_value in speak_as_values:
                    if speak_as_value == 'spell-out':
                        self._speak_as_spell_out_inherit(element)
                    elif speak_as_value == 'literal-punctuation':
                        self._speak_as_literal_punctuation_inherit(element)
                    elif speak_as_value == 'no-punctuation':
                        self._speak_as_no_punctuation_inherit(element)
                    elif speak_as_value == 'digits':
                        self._speak_as_digits_inherit(element)
        if rule.has_property('speak-punctuation'):
            declarations = rule.get_declarations('speak-punctuation')
            for declaration in declarations:
                property_value = declaration.get_value()
                if property_value == 'code':
                    self._speak_as_literal_punctuation_inherit(element)
                elif property_value == 'none':
                    self._speak_as_no_punctuation_inherit(element)
        if rule.has_property('speak-numeral'):
            declarations = rule.get_declarations('speak-numeral')
            for declaration in declarations:
                property_value = declaration.get_value()
                if property_value == 'digits':
                    self._speak_as_digits_inherit(element)
                elif property_value == 'continuous':
                    self._speak_as_continuous_inherit(element)
        if rule.has_property('speak-header'):
            declarations = rule.get_declarations('speak-header')
            for declaration in declarations:
                property_value = declaration.get_value()
                if property_value == 'always':
                    self._speak_header_always_inherit(element)
                elif property_value == 'once':
                    self._speak_header_once_inherit(element)

    def provide_speak_properties(self, element):
        rules = self.css_parser.get_rules([
            'speak',
            'speak-punctuation',
            'speak-numeral',
            'speak-header',
            'speak-as'
        ])
        for rule in rules:
            speak_elements = self.html_parser.find(
                rule.get_selector()
            ).list_results()
            for speak_element in speak_elements:
                if speak_element == element:
                    self._provide_speak_properties_with_rule(element, rule)
                    break

    def provide_all_speak_properties(self):
        selector = None
        rules = self.css_parser.get_rules([
            'speak',
            'speak-punctuation',
            'speak-numeral',
            'speak-header',
            'speak-as'
        ])
        for rule in rules:
            if selector is None:
                selector = rule.get_selector()
            else:
                selector = selector + ',' + rule.get_selector()
        if selector is not None:
            elements = self.html_parser.find(selector).list_results()
            for element in elements:
                if CommonFunctions.is_valid_element(element):
                    self.provide_speak_properties(element)
