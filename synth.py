# Copyright 2019 Google LLC
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

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
from synthtool import gcp

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()


# ----------------------------------------------------------------------------
# Generate datacatalog GAPIC layer
# ----------------------------------------------------------------------------
versions = ['v1', 'v1beta1']
for version in versions:
    library = gapic.py_library(
        'datacatalog',
        version,
    )

    s.move(
        library,
        excludes=[
            'docs/conf.py',
            'docs/index.rst',
            'README.rst',
            'nox*.py',
            'setup.py',
            'setup.cfg',
        ],
    )

# Fix docstring issue for classes with no summary line
s.replace(
    "google/cloud/**/proto/*_pb2.py",
    ''''__doc__': """Attributes:''',
    '''"__doc__": """
    Attributes:''',
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    cov_level=79,
    samples_test=True,
)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
