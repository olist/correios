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


class PackageError:
    def __init__(self, messages: str) -> None:
        self.messages = messages

    def __str__(self) -> str:
        return self.messages


class PackageDimensionError(PackageError):
    def __init__(self, name: str, value: int, min_value: int, max_value: int) -> None:
        self.name = name
        self.value = value
        self.min_value = min_value
        self.max_value = max_value

    def __str__(self) -> str:
        msg = 'Invalid {} (range: {}-{}, value: {})'
        return msg.format(self.name, self.min_value, self.max_value, self.value)


class PackageWeightError(PackageError):
    def __init__(self, service_code: str, value: int, min_value: int, max_value: int) -> None:
        self.service_code = service_code
        self.value = value
        self.min_value = min_value
        self.max_value = max_value

    def __str__(self) -> str:
        if self.service_code and self.max_value:
            msg = 'Invalid weight for the service {} (range: {}-{}, value: {})'
            return msg.format(self.service_code, self.min_value, self.max_value, self.value)

        msg = 'Invalid weight (min: {}, value: {})'
        return msg.format(self.min_value, self.value)
