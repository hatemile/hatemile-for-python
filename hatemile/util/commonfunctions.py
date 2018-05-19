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

import re

class CommonFunctions:
    """
    The CommonFuncionts class contains the used methods by HaTeMiLe classes.
    """

    count = 0

    @staticmethod
    def generateId(element, prefix):
        """
        Generate a id for a element.
        @param element: The element.
        @type element: L{hatemile.util.HTMLDOMElement}
        @param prefix: The prefix of id.
        @type prefix: str
        """

        if not element.hasAttribute('id'):
            element.setAttribute('id', prefix + str(CommonFunctions.count))
            CommonFunctions.count += 1

    @staticmethod
    def resetCount():
        """
        Reset the count number of ids.
        """

        CommonFunctions.count = 0

    @staticmethod
    def setListAttributes(element1, element2, attributes):
        """
        Copy a list of attributes of a element for other element.
        @param element1: The element that have attributes copied.
        @type element1: L{hatemile.util.HTMLDOMElement}
        @param element2: The element that copy the attributes.
        @type element2: L{hatemile.util.HTMLDOMElement}
        @param attributes: The list of attributes that will be copied.
        @type attributes: array.str
        """

        for attribute in attributes:
            if element1.hasAttribute(attribute):
                element2.setAttribute(attribute, element1.getAttribute(attribute))

    @staticmethod
    def increaseInList(listToIncrease, stringToIncrease):
        """
        The list of attributes that will be copied.
        @param listToIncrease: The list.
        @type listToIncrease: str
        @param stringToIncrease: The value of item.
        @type stringToIncrease: str
        @return: The list with the item added, if the item not was contained
        in list.
        @rtype: str
        """

        if (bool(listToIncrease)) and (bool(stringToIncrease)):
            if CommonFunctions.inList(listToIncrease, stringToIncrease):
                return listToIncrease
            else:
                return listToIncrease + ' ' + stringToIncrease
        elif bool(listToIncrease):
            return listToIncrease
        else:
            return stringToIncrease

    @staticmethod
    def inList(listToSearch, stringToSearch):
        """
        Verify if the list contains the item.
        @param listToSearch: The list.
        @type listToSearch: str
        @param stringToSearch: The value of item.
        @type stringToSearch: str
        @return: True if the list contains the item or false is not contains.
        @rtype: bool
        """

        if (bool(listToSearch)) and (bool(stringToSearch)):
            elements = re.split('[ \n\t\r]+', listToSearch)
            for element in elements:
                if element == stringToSearch:
                    return True
        return False
