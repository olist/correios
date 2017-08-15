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


import os

from vcr import VCR

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


vcr = VCR(
    record_mode='once',
    serializer='yaml',
    cassette_library_dir=os.path.join(FIXTURES_DIR, 'cassettes'),
    path_transformer=VCR.ensure_suffix('.yaml'),
    match_on=['method']
)
