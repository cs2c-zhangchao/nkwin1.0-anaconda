# root password spoke class
#
# Copyright (C) 2012 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Jesse Keating <jkeating@redhat.com>
#

# pylint: disable-msg=E0611
from gi.repository import Gtk

from pyanaconda.i18n import _, N_
from pyanaconda.users import cryptPassword, validatePassword
from pwquality import PWQError

from pyanaconda.ui.gui.spokes import NormalSpoke
from pyanaconda.ui.gui.categories.user_settings import UserSettingsCategory
from pyanaconda.ui.common import FirstbootSpokeMixIn

import pwquality

__all__ = ["NeokylinSpoke"]


class NeokylinSpoke(FirstbootSpokeMixIn, NormalSpoke):
    builderObjects = ["passwordWindow"]

    mainWidgetName = "passwordWindow"
    uiFile = "spokes/password.glade" 

    category = UserSettingsCategory

    icon = None
    title = None 

    def __init__(self, *args):
        NormalSpoke.__init__(self, *args)

    def initialize(self):
        pass

    def refresh(self):
        pass

    @property
    def status(self):
        return None

    @property
    def mandatory(self):
        return not any(user for user in self.data.user.userList
                            if "wheel" in user.groups)

    def apply(self):
        pass

    @property
    def completed(self):
        return True 


    def _checkPassword(self, editable = None, data = None):
        pass

    def on_back_clicked(self, button):
        pass
