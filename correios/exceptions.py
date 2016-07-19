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


class BaseCorreiosException(Exception):
    pass


class ModelException(BaseCorreiosException):
    pass


class ClientException(BaseCorreiosException):
    pass


class InvalidZipCodeException(ModelException):
    pass


class InvalidStateException(ModelException):
    pass


class InvalidFederalTaxNumberException(ModelException):
    pass


class InvalidStateTaxNumberException(ModelException):
    pass


class InvalidTrackingCode(ModelException):
    pass


class InvalidAddressesException(ModelException):
    pass


class InvalidVolumeInformation(ModelException):
    pass


class InvalidExtraServiceException(ModelException):
    pass


class PostingListError(ModelException):
    pass


class PostingListClosingError(ClientException):
    pass
