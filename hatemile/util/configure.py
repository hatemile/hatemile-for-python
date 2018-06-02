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

import os
from xml.dom import minidom
from .selectorchange import SelectorChange
from .skipper import Skipper


class Configure:
    """
    The Configure class contains the configuration of HaTeMiLe.
    """

    def __init__(self, file_name=None):
        """
        Initializes a new object that contains the configuration of HaTeMiLe.
        @param file_name: The full path of file.
        @type file_name: str
        """

        self.parameters = {}
        self.selector_changes = []
        self.skippers = []
        if file_name is None:
            file_name = os.path.dirname(os.path.dirname(os.path.dirname(
                os.path.realpath(__file__)
            ))) + '/hatemile-configure.xml'
        xmldoc = minidom.parse(file_name)
        params = xmldoc.getElementsByTagName(
            'parameters'
        )[0].getElementsByTagName('parameter')
        for param in params:
            if param.hasChildNodes():
                self.parameters[
                    param.attributes['name'].value
                ] = param.firstChild.nodeValue
            else:
                self.parameters[param.attributes['name'].value] = ''
        changes = xmldoc.getElementsByTagName(
            'selector-changes'
        )[0].getElementsByTagName('selector-change')
        for change in changes:
            self.selector_changes.append(SelectorChange(
                change.attributes['selector'].value,
                change.attributes['attribute'].value,
                change.attributes['value-attribute'].value
            ))
        skippers = xmldoc.getElementsByTagName(
            'skippers'
        )[0].getElementsByTagName('skipper')
        for skipper in skippers:
            self.skippers.append(Skipper(
                skipper.attributes['selector'].value,
                skipper.attributes['default-text'].value,
                skipper.attributes['shortcut'].value
            ))

    def get_parameters(self):
        """
        Returns the parameters of configuration.
        @return: The parameters of configuration.
        @rtype: dict
        """

        return self.parameters.copy()

    def get_parameter(self, name):
        """
        Returns the value of a parameter of configuration.
        @param name: The parameter.
        @type name: str
        @return: The value of the parameter.
        @rtype: str
        """

        return self.parameters[name]

    def get_selector_changes(self):
        """
        Returns the changes that will be done in selectors.
        @return: The changes that will be done in selectors.
        @rtype: array.L{hatemile.util.SelectorChange}
        """

        return [] + self.selector_changes

    def get_skippers(self):
        """
        Returns the skippers.
        @return: The skippers.
        @rtype: array.L{hatemile.util.Skipper}
        """

        return [] + self.skippers
