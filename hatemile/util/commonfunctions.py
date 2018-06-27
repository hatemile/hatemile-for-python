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
Module of CommonFunctions class.
"""

import re


class CommonFunctions:
    """
    The CommonFunctions class contains the used methods by HaTeMiLe classes.
    """

    #: The name of attribute for not modify the elements.
    DATA_IGNORE = 'data-ignoreaccessibilityfix'

    @staticmethod
    def set_list_attributes(element1, element2, attributes):
        """
        Copy a list of attributes of a element for other element.

        :param element1: The element that have attributes copied.
        :type element1: hatemile.util.html.htmldomelement.HTMLDOMElement
        :param element2: The element that copy the attributes.
        :type element2: hatemile.util.html.htmldomelement.HTMLDOMElement
        :param attributes: The list of attributes that will be copied.
        :type attributes: list(str)
        """

        for attribute in attributes:
            if element1.has_attribute(attribute):
                element2.set_attribute(
                    attribute,
                    element1.get_attribute(attribute)
                )

    @staticmethod
    def increase_in_list(list_to_increase, string_to_increase):
        """
        Increase a item in a HTML list.

        :param list_to_increase: The list.
        :type list_to_increase: str
        :param string_to_increase: The value of item.
        :type string_to_increase: str
        :return: The HTML list with the item added, if the item not was
                 contained in list.
        :rtype: str
        """

        if (bool(list_to_increase)) and (bool(string_to_increase)):
            if CommonFunctions.in_list(list_to_increase, string_to_increase):
                return list_to_increase
            return list_to_increase + ' ' + string_to_increase
        elif bool(list_to_increase):
            return list_to_increase
        return string_to_increase

    @staticmethod
    def in_list(list_to_search, string_to_search):
        """
        Verify if the list contains the item.

        :param list_to_search: The list.
        :type list_to_search: str
        :param string_to_search: The value of item.
        :type string_to_search: str
        :return: True if the list contains the item or False is not contains.
        :rtype: bool
        """

        if (bool(list_to_search)) and (bool(string_to_search)):
            elements = re.split('[ \n\t\r]+', list_to_search)
            for element in elements:
                if element == string_to_search:
                    return True
        return False

    @staticmethod
    def is_valid_element(element):
        """
        Check that the element can be manipulated by HaTeMiLe.

        :param element: The element
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :return: True if element can be manipulated or False if element cannot
                 be manipulated.
        :rtype: bool
        """

        if element.has_attribute(CommonFunctions.DATA_IGNORE):
            return False
        else:
            parent_element = element.get_parent_element()
            if parent_element is not None:
                tag_name = parent_element.get_tag_name()
                if (tag_name != 'BODY') and (tag_name != 'HTML'):
                    return CommonFunctions.is_valid_element(parent_element)
                return True
            return True
