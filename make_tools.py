#!/usr/bin/env python
# Copyright 2016 Google Inc. All rights reserved.
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

"""Creates pyfastboot.zip and fastboot.zip as standalone executables.

These files can be executed via:
  python pyfastboot.zip devices

The same way one would have run:
  python pyfastboot_debug.py devices

The zips can be transferred to other computers (and other CPU architectures) for
CPU and OS agnostic execution.
"""

import os
import sys
import zipfile


THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
  os.chdir(THIS_DIR)
  with zipfile.ZipFile('fastboot.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    z.write('pyfastboot/__init__.py')
    z.write('pyfastboot/common.py')
    z.write('pyfastboot/common_cli.py')
    z.write('pyfastboot/fastboot.py')
    z.write('pyfastboot/fastboot_debug.py', '__main__.py')
    z.write('pyfastboot/fastboot_extras.py')
    z.write('pyfastboot/usb_exceptions.py')
  return 0


if __name__ == '__main__':
  sys.exit(main())
