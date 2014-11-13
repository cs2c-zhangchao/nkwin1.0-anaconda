# The main file for anaconda TUI interface
#
# Copyright (C) (2012)  Red Hat, Inc.
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
# Red Hat Author(s): Martin Sivak <msivak@redhat.com>
#

from pyanaconda import ui
from pyanaconda.i18n import _
from pyanaconda.ui import common
from pyanaconda.ui.communication import hubQ
from pyanaconda.flags import flags
import simpleline as tui
from hubs.summary import SummaryHub
from hubs.progress import ProgressHub
from spokes import StandaloneSpoke
from tuiobject import YesNoDialog, ErrorDialog

import os
import sys
import site
import meh.ui.text

def exception_msg_handler(event, data):
    """
    Handler for the HUB_CODE_EXCEPTION message in the hubQ.

    :param event: event data
    :type event: (event_type, message_data)
    :param data: additional data
    :type data: any

    """

    # get data from the event data structure
    (event_type, msg_data) = event

    # msg_data is a list
    sys.excepthook(*msg_data[0])

class TextUserInterface(ui.UserInterface):
    """This is the main class for Text user interface."""

    ENVIRONMENT = "anaconda"

    def __init__(self, storage, payload, instclass,
                 productTitle = u"Anaconda", isFinal = True,
                 quitMessage = None):
        """
        For detailed description of the arguments see
        the parent class.

        :param storage: storage backend reference
        :type storage: instance of pyanaconda.Storage

        :param payload: payload (usually yum) reference
        :type payload: instance of payload handler

        :param instclass: install class reference
        :type instclass: instance of install class

        :param productTitle: the name of the product
        :type productTitle: unicode string

        :param isFinal: Boolean that marks the release
                        as final (True) or development
                        (False) version.
        :type isFinal: bool
        
        :param quitMessage: The text to be used in quit
                            dialog question. It should not
                            be translated to allow for change
                            of language.
        :type quitMessage: unicode string


        """

        ui.UserInterface.__init__(self, storage, payload, instclass)
        self._app = None
        self._meh_interface = meh.ui.text.TextIntf()

        self.productTitle = productTitle
        self.isFinal = isFinal
        self.quitMessage = quitMessage

    basemask = "pyanaconda.ui.tui"
    basepath = os.path.dirname(__file__)
    updatepath = "/tmp/updates/pyanaconda/ui/tui"
    sitepackages = [os.path.join(dir, "pyanaconda", "ui", "tui")
                    for dir in site.getsitepackages()]
    pathlist = set([updatepath, basepath] + sitepackages)

    paths = ui.UserInterface.paths + {
            "spokes": [(basemask + ".spokes.%s",
                        os.path.join(path, "spokes"))
                        for path in pathlist],
            "hubs": [(basemask + ".hubs.%s",
                      os.path.join(path, "hubs"))
                      for path in pathlist]
            }

    @property
    def tty_num(self):
        return 1

    @property
    def meh_interface(self):
        return self._meh_interface

    def _list_hubs(self):
        """returns the list of hubs to use"""
        return [SummaryHub, ProgressHub]

    def _is_standalone(self, spoke):
        """checks if the passed spoke is standalone"""
        return isinstance(spoke, StandaloneSpoke)

    def setup(self, data):
        """Construct all the objects required to implement this interface.
           This method must be provided by all subclasses.
        """
        self._app = tui.App(self.productTitle, yes_or_no_question = YesNoDialog,
                            quit_message = self.quitMessage, queue = hubQ.q)

        # tell python-meh it should use our raw_input
        self._meh_interface.set_io_handler(meh.ui.text.IOHandler(in_func=self._app.raw_input))

        # register handler for the exception messages
        self._app.register_event_handler(hubQ.HUB_CODE_EXCEPTION, exception_msg_handler)
        _hubs = self._list_hubs()

        # First, grab a list of all the standalone spokes.
        path = os.path.join(os.path.dirname(__file__), "spokes")
        spokes = self._collectActionClasses(self.paths["spokes"], StandaloneSpoke)
        actionClasses = self._orderActionClasses(spokes, _hubs)

        for klass in actionClasses:
            obj = klass(self._app, data, self.storage, self.payload, self.instclass)

            # If we are doing a kickstart install, some standalone spokes
            # could already be filled out.  In taht case, we do not want
            # to display them.
            if self._is_standalone(obj) and obj.completed:
                del(obj)
                continue

            if hasattr(obj, "set_path"):
                obj.set_path("spokes", self.paths["spokes"])

            obj.setup(self.ENVIRONMENT)

            self._app.schedule_screen(obj)

    def run(self):
        """Run the interface.  This should do little more than just pass
           through to something else's run method, but is provided here in
           case more is needed.  This method must be provided by all subclasses.
        """
        return self._app.run()

    ###
    ### MESSAGE HANDLING METHODS
    ###
    def showError(self, message):
        """Display an error dialog with the given message.  After this dialog
           is displayed, anaconda will quit.  There is no return value.  This
           method must be implemented by all UserInterface subclasses.

           In the code, this method should be used sparingly and only for
           critical errors that anaconda cannot figure out how to recover from.
        """
        error_window = ErrorDialog(self._app, message)
        self._app.switch_screen(error_window)

    def showDetailedError(self, message, details):
        self.showError(message + "\n\n" + details)

    def showYesNoQuestion(self, message):
        """Display a dialog with the given message that presents the user a yes
           or no choice.  This method returns True if the yes choice is selected,
           and False if the no choice is selected.  From here, anaconda can
           figure out what to do next.  This method must be implemented by all
           UserInterface subclasses.

           In the code, this method should be used sparingly and only for those
           times where anaconda cannot make a reasonable decision.  We don't
           want to overwhelm the user with choices.

           When cmdline mode is active, the default will be to answer no.
        """
        if flags.automatedInstall and not flags.ksprompt:
            # If we're in cmdline mode, just say no.
            return False
        question_window = YesNoDialog(self._app, message)
        self._app.switch_screen_modal(question_window)
        return question_window.answer
