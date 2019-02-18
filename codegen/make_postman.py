# -*- coding: utf-8 -*-
# Copyright 2019 Ross Jacobs All Rights Reserved.
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
"""Generate Postman collection with OpenAPI 3 JSON.

For more information, read
    https://github.com/postmanlabs/openapi-to-postman
"""
import subprocess as sp
import shutil
import tempfile


def make_postman_collection(src, options, verbosity=False):
    """Create a postman collection based on an OpenAPI3 JSON.

    Requires that node/npm be installed.
    Install openapi-to-postmanv2 to a temp dir, which is deleted when done.
    Prefer to send stderr to stdout so user can see them.

    Args:
        src (str): Full path of OpenAPI3 JSON
        options (str): String of openapi2postman options formatted
            like '-option value -option2 value2'. For available options:
            https://github.com/postmanlabs/openapi-to-postman#options
        verbosity (bool): Whether

    Raises:
        EnvironmentError: node is required. Quit if not found.
    """
    if not shutil.which('node'):
        raise EnvironmentError('Required node not found!')

    with tempfile.TemporaryDirectory() as tmpdir:
        print("Installing openapi-to-postmanv2 to a temp dir...")
        shutil.copy(src, tmpdir)
        install_cmds = ['npm', 'install', '--prefix',
                        tmpdir, 'openapi-to-postmanv2']
        with sp.Popen(install_cmds, stderr=sp.STDOUT) as sp_pipe:
            sp_pipe.communicate()

        print("Converting OpenAPI3 to Postman...")
        openapi2postman = tmpdir + \
            '/node_modules/openapi-to-postmanv2/bin/openapi2postmanv2.js'
        openapi2postman_cmds = ['node', openapi2postman, '-s', src]
        if options:
            openapi2postman_cmds += options.split(' ')
        with sp.Popen(openapi2postman_cmds, stderr=sp.STDOUT) as sp_pipe:
            sp_pipe.communicate()

    print("Postman collection successfully created! Temporary files deleted.")

