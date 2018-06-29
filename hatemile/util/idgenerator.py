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
Module of IDGenerator class.
"""

import uuid
from hatemile import helper


class IDGenerator:
    """
    The IDGenerator class generate ids for
    :py:class:`hatemile.util.html.HTMLDOMElement`.
    """

    def __init__(self, prefix_part=None):
        """
        Initializes a new object that generate ids for elements.

        :param prefix_part: A part of prefix id.
        :type prefix_part: str
        """

        helper.require_valid_type(prefix_part, str)

        if prefix_part is None:
            self.prefix_id = 'id-hatemile-' + IDGenerator.get_random() + '-'
        else:
            self.prefix_id = (
                'id-hatemile-'
                + prefix_part
                + '-'
                + IDGenerator.get_random()
                + '-'
            )
        self.count = 0

    @staticmethod
    def get_random():
        """
        Returns the random prefix.

        :return: The random prefix.
        :rtype: str
        """

        return uuid.uuid4().hex + uuid.uuid4().hex

    def generate_id(self, element):
        """
        Generate a id for a element.

        :param element: The element.
        :type element: hatemile.util.html.HTMLDOMElement
        """

        if not element.has_attribute('id'):
            element.set_attribute('id', self.prefix_id + str(self.count))
            self.count = self.count + 1
