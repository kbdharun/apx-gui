# main.py
#
# Copyright 2023 Mirko Brombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
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
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi
import logging
from gettext import gettext as _

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('GtkSource', '5')

from gi.repository import Gtk, GLib, Gio, Adw
from apx_ide.windows.main_window import ApxIDEWindow


logging.basicConfig(level=logging.INFO)


class ApxIDEApplication(Adw.Application):
    """The main application singleton class."""

    __embedded: bool = False

    def __init__(self):
        super().__init__(application_id='org.vanillaos.ApxIDE',
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE)
        
        self.__window: ApxIDEWindow = None

        self.create_action('quit', self.close, ['<primary>q'])
        self.create_action('new_subsystem', self.on_new_subsystem_action, ['<primary>n'])
        self.create_action('new_stack', self.on_new_stack_action, ['<primary>s'])
        self.create_action('new_pkgmanager', self.on_new_pkgmanager_action, ['<primary>p']) 
        self.create_action('about', self.on_about_action, ['<primary>a'])

        self.__register_arguments()

    def __register_arguments(self):
        """Register command line arguments."""
        self.add_main_option("embedded", ord("e"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Embedded mode", None)

    def do_command_line(self, command: Gio.ApplicationCommandLine) -> int:
        """Handle command line arguments.

        We only have one command line option, --embedded, which
        indicates that the application is embedded in another
        application.
        """
        commands = command.get_options_dict()

        if commands.contains("embedded"):
            self.__embedded = True

        self.do_activate()
        return 0

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = ApxIDEWindow(application=self,
                               embedded=self.__embedded)

        self.__window = win
        win.present()

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Apx IDE',
                                application_icon='org.vanillaos.ApxIDE',
                                developer_name='Mirko Brombin',
                                website='https://github.com/Vanilla-OS/apx-gui',
                                issue_url='https://github.com/Vanilla-OS/apx-gui/issues',
                                version='1.0.2',
                                developers=['Mirko Brombin https://github.com/mirkobrombin/'],
                                translator_credits= _("translator_credits"),
                                copyright='© 2023 Mirko Brombin and Contributors',
                                license_type=('gpl-3-0-only'))
        about.add_credit_section(
            _("Contributors"),
            [
                "K.B.Dharun Krishna https://github.com/kbdharun",
            ]
        )
        about.add_acknowledgement_section(
            _("Tools"),
            [
                "apx https://github.com/Vanilla-OS/apx",
            ]
        )
        about.present()

    def on_new_subsystem_action(self, *args):
        self.__window.new_subsystem()

    def on_new_stack_action(self, *args):
        self.__window.new_stack()
    
    def on_new_pkgmanager_action(self, *args):
        self.__window.new_pkgmanager()

    def create_action(self, name: str, callback: callable, shortcuts: list[str] = None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def close(self, *args):
        """Close the application."""
        self.quit()

def main(version: str):
    """The application's entry point."""
    app = ApxIDEApplication()
    return app.run(sys.argv)
