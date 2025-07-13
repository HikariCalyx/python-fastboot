pyfastboot
==========

This is a modified version for specific project usage - for example, service permission granting program for all Nokia phones.

For ADB implementation, see [adb_shell](https://github.com/JeffLIrion/adb_shell).

This repository contains a pure-python implementation of the Fastboot
protocols, using libusb1 for USB communications.

This is a complete replacement and rearchitecture of the Android project's [ADB
and fastboot code](https://github.com/android/platform_system_core/tree/master/adb)

This code is mainly targeted to users that need to communicate with Android
devices in an automated fashion, such as in automated testing. 


### Using as standalone tool

Once installed, one new binary should be available:  `pyfastboot`.

Running `./make_tools.py` creates one file: `fastboot.zip`. They
can be run similar to native `fastboot` via the python interpreter:

    python fastboot.zip oem device-info

### Using as a Python Library

FIHSW model: [See this file as reference](https://github.com/HikariCalyx/uu4-linux/blob/main/auth_utility/fihGetPermission.py)

HMDSW model get permission code (note the dk_calculation module is unavailable yet).

```python
from pyfastboot import fastboot
from io import StringIO
import dk_calculation
import sys

def _InfoCb(message):
    if not message.message:
        return
    print(message.message.decode('utf-8'))

def getsecver(device):
    tmp = sys.stdout
    result = StringIO()
    sys.stdout = result
    device.Oem('getsecurityversion', info_cb=_InfoCb)
    sys.stdout = tmp
    del tmp
    return result.getvalue().splitlines()

def getperm(device):
    tmp = sys.stdout
    result = StringIO()
    sys.stdout = result
    device.Oem('getpermissions', info_cb=_InfoCb)
    sys.stdout = tmp
    del tmp
    return result.getvalue().splitlines()

def authcode(device):
    return device.HmdAuthStart().decode('utf-8')

ThisDevice = fastboot.FastbootCommands()
ThisDevice.ConnectDevice()

# Essential Informations will be stored at these 3 variables.

product = ThisDevice.Getvar('product').decode('utf-8')
secver = getsecver(ThisDevice)[0]
psn = ThisDevice.Getvar('serialno').decode('utf-8')

# 1st permission type is flash
ThisDevice.HmdEnableAuth(1, dk_calculation.getresult(prjcode=product, serialnumber=psn, securityversion=secver, auth_code=authcode(ThisDevice))

# Check Enabled Permissions
print(getperm(ThisDevice))

# 3rd permission type is repair
ThisDevice.HmdEnableAuth(3, dk_calculation.getresult(prjcode=product, serialnumber=psn, securityversion=secver, auth_code=authcode(ThisDevice))

# Check Enabled Permissions
print(getperm(ThisDevice))
```



### Pros

  * Simpler code due to use of libusb1 and Python.
  * API can be used by other Python code easily.
  * Errors are propagated with tracebacks, helping debug connectivity issues.
  * No daemon outliving the command.
  * Can be packaged as standalone zips that can be run independent of the CPU
    architecture (e.g. x86 vs ARM).


### Cons

  * Technically slower due to Python, mitigated by no daemon.
  * Only one command per device at a time.

### Dependencies

  * libusb1 (1.0.16+)
  * python-libusb1 (1.2.0+)
  * `fastboot.zip` (optional):
    * python-progressbar (2.3+)

### History

#### 1.3.13

* Added new feature: Brand specific OEM command function `BrandCommand(brand, command)`.
  * Example:
```python
# Bootloader unlock for Hisense Phones
ThisDevice.BrandCommand('Hisense', 'unlock')

# Bootloader unlock for early Vivo Phones
ThisDevice.BrandCommand('bbk', 'unlock_vivo')

# Bootloader unlock for recent Vivo / IQOO Phones
ThisDevice.BrandCommand('vivo_bsp', 'unlock_vivo')
```

#### 1.3.12

* Added new feature: Automatically merge Len smartphone getvar all dict, return Hmd GetDevInfo command into a proper dict.

#### 1.3.11

* Fixed the issue on device without Fastbootd mode cannot pass isFastbootdCheck.

#### 1.3.10

* Fixed dependencies issue.
* Fixed the Getvar function issue.
* Add new feature: logical-partition create, resize and delete under fastbootd. (CreateLogicalPartition, ResizeLogicalPartition, DeleteLogicalPartition)

#### 1.3.8

* Added support for Unisoc "flashing unlock_bootloader" function (UnisocUnlockBootloader())
* Added support for vbmeta processing
* Fixed issue of GetIdentifierToken function

#### 1.3.6

* Fixed dependencies bug
* Added initial support of GetIdentifierToken function for HTC and Unisoc models (GetIdentifierToken())

#### 1.3.5

* Renaming it into pyfastboot
* Add Nokia, Motorola and Xiaomi specific OEM command functions