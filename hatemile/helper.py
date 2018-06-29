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
Helper methods of HaTeMiLe for Python.
"""


def require_not_none(*values):
    """
    Checks that the specified objects references is not None and throws a
    :py:class:`ValueError` if it is.

    :param values: The objects.
    :type values: list(object)
    """

    for value in values:
        if value is None:
            raise ValueError()


def require_valid_type(value, *classes):
    """
    Checks that the specified object reference is instance of classes and
    throws a :py:class:`TypeError` if it is not.

    :param value: The object.
    :type value: object
    :param classes: The classes.
    :type classes: list(class)
    """

    if value is not None:
        valid = False
        for auxiliar_class in classes:
            if isinstance(value, auxiliar_class):
                valid = True
                break
        if not valid:
            raise TypeError()
