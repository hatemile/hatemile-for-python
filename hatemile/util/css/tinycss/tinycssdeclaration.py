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
Module of TinyCSSDeclaration.
"""

import re
from tinycss.css21 import Declaration
from hatemile import helper
from hatemile.util.css.stylesheetdeclaration import StyleSheetDeclaration


class TinyCSSDeclaration(StyleSheetDeclaration):
    """
    The TinyCSSDeclaration class is official implementation of
    :py:class:`hatemile.util.css.stylesheetdeclaration.StyleSheetDeclaration`
    for tinycss.
    """

    def __init__(self, declaration):
        """
        Initializes a new object that encapsulate the tinycss declaration.

        :param declaration: The tinycss declaration.
        :type declaration: tinycss.css21.Declaration
        """

        helper.require_not_none(declaration)
        helper.require_valid_type(declaration, Declaration)

        self.declaration = declaration

    def get_value(self):
        return self.declaration.value.as_css()

    def get_values(self):
        return re.split('[ \n\t\r]+', self.get_value())

    def get_property(self):
        return self.declaration.name
