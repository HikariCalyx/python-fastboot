#!/usr/bin/env python
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

"""
Additional Implementations for Python-Fastboot
"""

class Constants(object):
    """Encapsulates constants, usually some specially crafted files."""

    def __init__(self):
        '''Init the Class'''

    @classmethod
    def misc_wipedata(self):
        """
        The misc partition that could trigger recovery mode to perform factory reset.
        Some devices that could not erase userdata partitions in few seconds can flash
        this into misc partition instead.

        Size: 85 bytes
        """
        return b'boot-recovery' + 51 * b'\0' + b'recovery\n--wipe_data\n'

    def misc_wipedata_b(self):
        """
        The misc partition that could trigger recovery mode to perform factory reset.
        Some devices that could not erase userdata partitions in few seconds can flash
        this into misc partition instead.

        This one is for unisoc models that will switch the slot to B as well.

        Size: 2,050 bytes
        """
        return b'boot-recovery' + 51 * b'\0' + b'recovery\n--wipe_data\n' + 0x7AB * b'\0' + b'_b'
    
    def frp_oemunlock(self):
        """
        The frp partition that could turn on OEM Unlocking in developer options.
        Only usable when you grant flash permission by secret OEM commands.

        Size: 524,288 bytes (512KB)
        """
        return b'\x40\xF5\xB6\x80\x53\x6B\xD7\x67\x53\xB2\xD9\x19\x79\x3E\x63\x66\x95\x5F\xB4\x38\x0E\xFE\xBF\xA5\x41\xDE\xD2\xD2\x29\xA4\xF5\x0F' + 0x7FFDF * b'\0' + b'\1'
    
    def config_oemunlock(self):
        """
        The config partition that could turn on OEM Unlocking in developer options.
        Only usable when you grant flash permission by secret OEM commands.

        Size: 32,768 bytes (32KB)
        """
        return b'\x09\xF9\x72\x9B\x31\x66\x9C\x63\xF2\xD8\x5F\x13\xAE\x9B\xF5\x39\x79\xCF\xBA\x43\x17\xB9\x9C\xB2\xFB\x76\x37\xC8\x89\x5E\x3E\x2A' + 0x7FDF * b'\0' + b'\1'


def FlagVbmeta(vbmeta_file, DisableVerity=True, DisableVerification=True):
    """
    Flags vbmeta file to disable verification.

    For vbmeta in raw bytes form, use the function FlagVbmetaBytes instead.

    Args:
      vbmeta_file: Path of vbmeta file or other files with vbmeta info attached.
        e.g. '/home/yourname/vbmeta.img'
      DisableVerity: Is dm-verity supposed to be disabled. Disabled by default.
      DisableVerification: Is verification supposed to be disabled. 
                           Disabled by default.

    Returns:
      Bytearray of vbmeta with either DisableVerity or DisableVerification flag
      applied depends on the preferences.
    """
    pass

def FlagVbmetaBytes(vbmeta_bytes, DisableVerity=True, DisableVerification=True):
    """
    Flags vbmeta bytes to disable verification.

    For vbmeta in actual file, use the function FlagVbmeta instead.

    Args:
      vbmeta_bytes: The byte of bytearray of vbmeta file.
        e.g. b'AVBh.......AVBf'
      DisableVerity: Is dm-verity supposed to be disabled. Disabled by default.
      DisableVerification: Is verification supposed to be disabled. 
                           Disabled by default.

    Returns:
      Bytearray of vbmeta with either DisableVerity or DisableVerification flag
      applied depends on the preferences.
    """
    pass
