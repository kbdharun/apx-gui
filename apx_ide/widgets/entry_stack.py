# entry_stack.py
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

from gi.repository import Gtk, Gio, GObject, Adw

from apx_ide.core.apx_entities import Stack


@Gtk.Template(resource_path='/org/vanillaos/apx-ide/gtk/entry-stack.ui')
class EntryStack(Adw.ActionRow):
    __gtype_name__: str = 'EntryStack'

    def __init__(self, stack: Stack, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_title(stack.name)

        self.stack: Stack = stack
        self.aid: UUID = stack.aid
