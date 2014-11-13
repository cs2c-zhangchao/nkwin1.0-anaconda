#
# rhel.py
#
# Copyright (C) 2010  Red Hat, Inc.  All rights reserved.
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
# Modification(s):
# No.1 
# Author(s): Xia Lei <lei.xia@cs2c.com.cn>
# Descriptions: - reset default partitioning.
#               - reset defaultFs to be ext4
#               - reset autopart type to be AUTOPART_TYPE_PLAIN
#               - add combo to be used to select partitioning scheme 
#                 on the customPartitioningSpoke gui.
#               - delete refresh button.
# Modificated file(s):pyanaconda/installclass.py,
#                     pyanaconda/installclasses/neokylin.py,
#                     pyanaconda/ui/gui/spokes/storage.py,
#                     pyanaconda/ui/gui/spokes/custom.py,
#                     pyanaconda/ui/gui/spokes/lib/according.py
#                     pyanaconda/ui/gui/spokes/custom.glade
# keywords: default partitioning; defaultFS; autopart type; add combo; delete refresh button

from pyanaconda.installclass import BaseInstallClass
from pyanaconda.constants import *
from pyanaconda.product import *
import types

class InstallClass(BaseInstallClass):
    # name has underscore used for mnemonics, strip if you dont need it
    id = "rhel"
    name = N_("Red Hat Enterprise Linux")
    sortPriority = 10000
    hidden = 1
    # nkwin7 add begin
    # keywords: default partitioning; defaultFS; autopart type; add combo; delete refresh button
    # reset defaultFs
    #defaultFS = "xfs"
    defaultFS = "ext4"
    # nkwin7 end

    bootloaderTimeoutDefault = 5
    bootloaderExtraArgs = []

    ignoredPackages = ["ntfsprogs"]

    _l10n_domain = "comps"

    efi_dir = "redhat"

    def configure(self, anaconda):
        BaseInstallClass.configure(self, anaconda)
        BaseInstallClass.setDefaultPartitioning(self, anaconda.storage)

    def __init__(self):
        BaseInstallClass.__init__(self)
