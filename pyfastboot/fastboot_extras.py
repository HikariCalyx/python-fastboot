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

from hashlib import sha256

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
    
    def image_oemunlock(self, length):
        """
        Generates partition image that could turn on OEM Unlocking in developer options.
        Only usable when you grant flash permission by secret OEM commands.

        Args:
          length: The size of the image size you want, Unit is bytes. 
          It needs to be divisible by 4,096.
          If cannot be divisible by 4,096, a slightly bigger file will be generated.

        Returns:
          Raw bytes that based on the length you provides.
        """
        if length % 4096 > 0:
            length = (length // 4096 + 1) * 4096
        sha256sum = bytes.fromhex(sha256((length - 1) * b'\0' + b'\1').hexdigest())
        return sha256sum + (length - 33) * b'\0' + b'\1'
    
    def frp_oemunlock(self):
        """
        The frp partition that could turn on OEM Unlocking in developer options.
        Only usable when you grant flash permission by secret OEM commands.

        Size: 524,288 bytes (512KB)
        """
        return Constants.image_oemunlock(self, 524288)
    
    def config_oemunlock(self):
        """
        The config partition that could turn on OEM Unlocking in developer options.
        Only usable when you grant flash permission by secret OEM commands.

        Size: 32,768 bytes (32KB)
        """
        return Constants.image_oemunlock(self, 32768)
    
    def mkfs(self, size, filesystem='e2fs'):
        """
        Creates the formatted partition image for flashing.

        Args:
          size: The partition size, Unit is bytes.
                It needs to be divisible by 4,096.
                If cannot be divisible by 4,096, a slightly bigger file will be generated.
          filesystem: Desired formatted filesystem, default is e2fs. Can also specify fat, fat32, f2fs.

        Returns:
          Formatted sparse image in bytearray form.

        It should be used altogether with Erase, ByteDownload function. Example:

        from pyfastboot import fastboot
        from pyfastboot import fastboot_extras as fe

        device = fastboot.FastbootCommands()
        device.ConnectDevice()
        device.Erase('userdata')
        try:
            device.ByteDownload(
                fe.Constants.mkfs(
                    int(device.Getvar(partition-size:userdata).decode('utf-8')), 
                    filesystem=device.Getvar(partition-type:userdata).decode('utf-8')
                )
            device.Flash('userdata')
        except Exception:
            pass
        """
        if filesystem not in ['ext4', 'e2fs', 'f2fs', 'fat', 'fat32']:
            raise Exception('NotValidFilesystemException')
        pass
   



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

    It should be used altogether with ByteDownload function. Example:
    
    from pyfastboot import fastboot
    from pyfastboot import fastboot_extras as fe

    device = fastboot.FastbootCommands()
    device.ConnectDevice()
    device.ByteDownload(fe.FlagVbmeta('/path/to/vbmeta.img', 
        DisableVerity=True, DisableVerification=True))
    device.Flash('vbmeta_a')

    """
    with open(vbmeta_file, 'rb') as f:
        vbmeta = f.read()
    return FlagVbmetaBytes(vbmeta, DisableVerity=DisableVerity, DisableVerification=DisableVerification)

def FlagVbmetaBytes(vbmeta_bytes, DisableVerity=True, DisableVerification=True):
    """
    Flags vbmeta bytes to disable verification.

    For vbmeta in actual file, use the function FlagVbmeta instead.

    Args:
      vbmeta_bytes: Raw bytes or bytearray of vbmeta file.
        e.g. b'AVB0.......AVBf'
      DisableVerity: Is dm-verity supposed to be disabled. Disabled by default.
      DisableVerification: Is verification supposed to be disabled. 
                           Disabled by default.

    Returns:
      Bytearray of vbmeta with either DisableVerity or DisableVerification flag
      applied depends on the preferences.
      
    It should be used altogether with ByteDownload function.
    """
    if DisableVerity and DisableVerification:
        Flag = b'\3'
    elif not DisableVerity and DisableVerification:
        Flag = b'\2'
    elif DisableVerity and not DisableVerification:
        Flag = b'\1'
    else:
        Flag = b'\0'
    AVBf = vbmeta_bytes[len(vbmeta_bytes)-64:]
    # rawImageLength = int(AVBf[0x10:0x14].hex(), 16)
    AVB0ImageBeginOffset = int(AVBf[0x18:0x1C].hex(), 16)
    vbmeta_part = vbmeta_bytes[0:123] + Flag + vbmeta_bytes[124:len(vbmeta_bytes)-64] + AVBf
    vbmeta_bytes = vbmeta_bytes[0:AVB0ImageBeginOffset]
    return vbmeta_bytes + vbmeta_part