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
Module of TinyCSSRule class.
"""

from tinycss.css21 import RuleSet
from hatemile import helper
from hatemile.util.css.stylesheetrule import StyleSheetRule
from .tinycssdeclaration import TinyCSSDeclaration


class TinyCSSRule(StyleSheetRule):
    """
    The TinyCSSRule class is official implementation of
    :py:class:`hatemile.util.css.stylesheetrule.StyleSheetRule` for tinycss.
    """

    def __init__(self, rule):
        """
        Initializes a new object that encapsulate the tinycss rule.

        :param rule: The tinycss rule.
        :type rule: tinycss.css21.RuleSet
        """

        helper.require_not_none(rule)
        helper.require_valid_type(rule, RuleSet)

        self.rule = rule

    def has_property(self, property_name):
        for declaration in self.rule.declarations:
            if declaration.name == property_name:
                return True
        return False

    def has_declarations(self):
        return bool(self.rule.declarations)

    def get_declarations(self, property_name):
        declarations = list()
        for declaration in self.rule.declarations:
            if declaration.name == property_name:
                declarations.append(TinyCSSDeclaration(declaration))
        return declarations

    def get_selector(self):
        return self.rule.selector.as_css()
