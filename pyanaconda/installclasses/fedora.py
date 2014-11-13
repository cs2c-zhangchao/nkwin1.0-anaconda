#
# fedora.py
#
# Copyright (C) 2007  Red Hat, Inc.  All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from pyanaconda.installclass import BaseInstallClass
from pyanaconda.constants import *
from pyanaconda.product import *
from pyanaconda import network
from pyanaconda import nm
from pyanaconda.i18n import _

import os, types

class InstallClass(BaseInstallClass):
    # name has underscore used for mnemonics, strip if you dont need it
    id = "fedora"
    name = N_("_Fedora")
    sortPriority = 10000
    if productName.startswith("Red Hat Enterprise"):
        hidden = 1

    _l10n_domain = "anaconda"

    efi_dir = "fedora"

    def configure(self, anaconda):
	BaseInstallClass.configure(self, anaconda)
        BaseInstallClass.setDefaultPartitioning(self, anaconda.storage)

    def setGroupSelection(self, anaconda):
        BaseInstallClass.setGroupSelection(self, anaconda)

    def setNetworkOnbootDefault(self, ksdata):
        # if something's already enabled, we can just leave the config alone
        for devName in nm.nm_devices():
            if not nm.nm_device_type_is_wifi(devName) and \
               network.get_ifcfg_value(devName, "ONBOOT", ROOT_PATH) == "yes":
                return

        # the default otherwise: bring up the first wired netdev with link
        for devName in nm.nm_devices():
            if nm.nm_device_type_is_wifi(devName):
                continue
            try:
                link_up = nm.nm_device_carrier(devName)
            except ValueError as e:
                continue
            if link_up:
                dev = network.NetworkDevice(ROOT_PATH + network.netscriptsDir, devName)
                dev.loadIfcfgFile()
                dev.set(('ONBOOT', 'yes'))
                dev.writeIfcfgFile()
                for nd in ksdata.network.network:
                    if nd.device == dev.iface:
                        nd.onboot = True
                        break
                break

    def __init__(self):
	BaseInstallClass.__init__(self)
