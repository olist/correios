# Copyright 2016 Osvaldo Santana Neto
#
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


from correios.exceptions import InvalidZipCode


class Zip(object):
    def __init__(self, code: str):
        self._code = None
        self.set_code(code)

    def get_code(self) -> str:
        return self._code

    def set_code(self, code: str):
        code = "".join(d for d in code if d.isdigit())
        if len(code) != 8:
            raise InvalidZipCode("Zip code must have 8 digits")
        self._code = code

    code = property(get_code, set_code)

    def display(self) -> str:
        return "{}-{}".format(self.code[:5], self.code[-3:])

    def __str__(self):
        return self.code

    def __repr__(self):
        return "<Zip code: {}>".format(self.code)
