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
Module of Configure class.
"""

import json
import locale
import os
from hatemile import helper


class Configure:
    """
    The Configure class contains the configuration of HaTeMiLe.
    """

    def __init__(self, file_name=None, locale_configuration=None):
        """
        Initializes a new object that contains the configuration of HaTeMiLe.

        :param file_name: The full path of file.
        :type file_name: str
        :param locale_configuration: The locale of configuration.
        :type locale_configuration: tuple(str, str)
        """

        helper.require_valid_type(file_name, str)
        helper.require_valid_type(locale_configuration, tuple)

        if file_name is None:
            if locale_configuration is not None:
                locale_code = locale_configuration[0]
            else:
                locale_code = locale.getdefaultlocale()[0]
            file_name = os.path.join(os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.realpath(__file__))
            )), '_locales', locale_code, 'configuration.json')
            if not os.path.isfile(file_name):
                file_name = os.path.join(os.path.dirname(os.path.dirname(
                    os.path.dirname(os.path.realpath(__file__))
                )), '_locales', 'en_US', 'configuration.json')
        with open(file_name, 'r') as json_file:
            self.parameters = json.load(json_file)

    def get_parameters(self):
        """
        Returns the parameters of configuration.

        :return: The parameters of configuration.
        :rtype: dict(str, str)
        """

        return self.parameters.copy()

    def has_parameter(self, parameter):
        """
        Check that the configuration has an parameter.

        :param parameter: The name of parameter.
        :type parameter: str
        :return: True if the configuration has the parameter or False if the
                 configuration not has the parameter.
        :rtype: bool
        """

        return parameter in self.parameters

    def get_parameter(self, parameter):
        """
        Returns the value of a parameter of configuration.

        :param parameter: The parameter.
        :type parameter: str
        :return: The value of the parameter.
        :rtype: str
        """

        return self.parameters[parameter]
