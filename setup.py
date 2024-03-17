# Copyright 2014 Google Inc. All rights reserved.
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

from setuptools import setup


setup(
    name = 'pyfastboot',
    packages = ['pyfastboot'],
    version = '1.3.5',
    author = 'Hikari Calyx',
    author_email = 'hikaricalyx@hikaricalyx.com',
    maintainer = 'Hikari Calyx',
    maintainer_email = 'hikaricalyx@hikaricalyx.com',
    url = 'https://github.com/HikariCalyx/python-adb',
    description = 'A pure python implementation of the Android Fastboot protocols',
    long_description = '''
This repository contains a pure-python implementation of the Android
ADB and Fastboot protocols, using libusb1 for USB communications.

Additionally, support for specific OEM commands were added, including Nokia, 
Motorola, and Xiaomi.

This is a complete replacement and rearchitecture of the Android
project's fastboot code available at
https://github.com/android/platform_system_core/tree/master/adb

This code is mainly targeted to users that need to communicate with
Android devices in an automated fashion, such as in automated
testing. 
''',

    keywords = ['android', 'fastboot'],

    install_requires = [
        'libusb1>=1.0.16'
    ],

    extra_requires = {
        'fastboot': 'progressbar>=2.3'
    },

## classifier list https://pypi.python.org/pypi?:action=list_classifiers
    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing'
    ],
    entry_points={
        "console_scripts": [
            "pyfastboot = pyfastboot.fastboot_debug:main",
        ],
    }

)
