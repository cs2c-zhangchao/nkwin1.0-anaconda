# Base classes for spoke categories.
#
# Copyright (C) 2011  Red Hat, Inc.
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
# Red Hat Author(s): Chris Lumens <clumens@redhat.com>
#

import os.path
from pyanaconda.i18n import N_
from pyanaconda.ui.common import collect

__all__ = ["SpokeCategory", "collect_categories"]

class SpokeCategory(object):
    """A SpokeCategory is an object used to group multiple related Spokes
       together on a hub.  It consists of a title displayed above, and then
       a two-column grid of SpokeSelectors.  Each SpokeSelector is associated
       with a Spoke subclass.  A SpokeCategory will only display those Spokes
       with a matching category attribute.

       Class attributes:

       displayOnHub  -- The Hub subclass to display this Category on.  If
                        None, this Category will be skipped.
       title         -- The title of this SpokeCategory, to be displayed above
                        the grid.
    """
    displayOnHub = None
    title = N_("DEFAULT TITLE")

def collect_categories(mask_paths):
    """Return a list of all category subclasses. Look for them in modules
       imported as module_mask % basename(f) where f is name of all files in path.
    """
    categories = []
    for mask, path in mask_paths:
        categories.extend(collect(mask, path, lambda obj: getattr(obj, "displayOnHub", None) != None))
        
    return categories
