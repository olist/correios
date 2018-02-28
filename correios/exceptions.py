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


class BaseCorreiosError(Exception):
    pass


class ModelError(BaseCorreiosError):
    pass


class ClientError(BaseCorreiosError):
    pass


class InvalidZipCodeError(ModelError):
    pass


class InvalidStateError(ModelError):
    pass


class InvalidFederalTaxNumberError(ModelError):
    pass


class InvalidStateTaxNumberError(ModelError):
    pass


class InvalidUserContractError(ModelError):
    pass


class InvalidTrackingCodeError(ModelError):
    pass


class InvalidShippingLabelError(ModelError):
    pass


class InvalidPackageError(ModelError):
    pass


class InvalidPackageDimensionsError(InvalidPackageError):
    pass


class InvalidMinPackageDimensionsError(InvalidPackageDimensionsError):
    pass


class InvalidMaxPackageDimensionsError(InvalidPackageDimensionsError):
    pass


class InvalidPackageWeightError(InvalidPackageError):
    pass


class InvalidMinPackageWeightError(InvalidPackageWeightError):
    pass


class InvalidMaxPackageWeightError(InvalidPackageWeightError):
    pass


class InvalidPackageSequenceError(InvalidPackageError):
    pass


class InvalidAddressesError(ModelError):
    pass


class InvalidExtraServiceError(ModelError):
    pass


class PostingListError(ModelError):
    pass


class InvalidRegionalDirectionError(ModelError):
    pass


class PostingListSerializerError(ClientError):
    pass


class TrackingCodesLimitExceededError(ClientError):
    pass


class AuthenticationError(ClientError):
    pass


class ConnectTimeoutError(ClientError):
    pass


class ClosePostingListError(ClientError):
    pass


class CanceledPostingCardError(ClientError):
    pass


class NonexistentPostingCardError(ClientError):
    pass


class RendererError(BaseCorreiosError):
    pass


class TrackingCodeNotFoundError(ModelError):
    pass


class InvalidEventStatusError(ModelError):
    pass


class InvalidDeclaredValueError(ModelError):
    pass


class MaximumDeclaredValueError(InvalidDeclaredValueError):
    pass


class MinimumDeclaredValueError(InvalidDeclaredValueError):
    pass
