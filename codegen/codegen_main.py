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
"""Main function."""
import subprocess as sp
import re

import codegen._cli as cli
import codegen.make_api_client as api_client
import codegen.make_openapi3_json as openapi3
import codegen.make_postman as postman


def main():
    """Main function."""
    check_requirements()
    args = cli.get_cli_args()
    available_langs = get_languages()
    invalid_langs = set().difference(set(available_langs))
    if invalid_langs:
        err_msg = "Valid languages on system: " + available_langs + \
            "\nInvalid entered languages: " + str(invalid_langs)
        raise SyntaxWarning(err_msg)

    openapi3_location = openapi3.make_spec('openapi3' in args['--spec'])
    if 'postman' in args['--spec']:
        postman.make_postman_collection(openapi3_location, args['--option'])

    if args['--lang']:
        api_client.download_openapi_generator()
        api_client.generate_api_clients(args['--lang'], openapi3_location)


def check_requirements():
    """Check the requirements
    
    Requirements:
        * java > 1.8
    """
    check_java_version()

    print('...Requirements satisfied!')


def check_java_version():
    """Verify whether Java version is correct."""
    required_java_version = 1.8
    java_version = get_java_version()
    if java_version < required_java_version:
        raise Exception("Required Java 1.8+ not found.")


def get_java_version():
    """Return the system java version."""
    cmd_list = ['java', '-version']
    version_text = str(sp.check_output(cmd_list, stderr=sp.STDOUT))
    if 'version' not in version_text:
        raise Exception("Java not found. Reinstall and try again.")
    version = re.search(r'"([\d]*\.[\d]*)\.[\d]*_', str(version_text))[1]
    
    return float(version)


def get_languages():
    """Get the languages that OpenAPI Generator supports.

    :returns list
    """
    cmd_list = 'java -jar openapi-generator-cli.jar langs'.split(' ')
    avail_languages_str = sp.check_output(cmd_list).decode('utf-8').strip()
    languages_str = avail_languages_str.split(': ')[1]
    languages_list = languages_str[1:-1].split(', ')  # Remove '[', ']'

    return languages_list


if __name__ == '__main__':
    main()