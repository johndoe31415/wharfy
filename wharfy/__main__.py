#	wharfy - Tiny Docker orchestration toolkit without Yaml
#	Copyright (C) 2025-2025 Johannes Bauer
#
#	This file is part of wharfy.
#
#	wharfy is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	wharfy is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with wharfy; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import sys
import wharfy
from .MultiCommand import MultiCommand
from .ActionStart import ActionStart
from .ActionConsole import ActionConsole
from .ActionBuild import ActionBuild

def main(argv = None):
	if argv is None:
		argv = sys.argv
	mc = MultiCommand(description = "Instrument Docker build and runtime", run_method = True, trailing_text = f"wharfy v{wharfy.VERSION}")

	def genparser(parser):
		parser.add_argument("-c", "--config-file", metavar = "filename", default = "wharfy.json", help = "Configuration file to use. Defaults to %(default)s.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be given multiple times.")
	mc.register("build", "Build some Wharfy containers", genparser, action = ActionBuild)

	def genparser(parser):
		parser.add_argument("-f", "--foreground", action = "store_true", help = "By default, the container is started as a daemon. This starts it in foreground with attached tty.")
		parser.add_argument("-r", "--remove-container", action = "store_true", help = "When a container by the same name already exists, starting will fail to preserve logs. With this option, containers are removed before starting a new one.")
		parser.add_argument("-c", "--config-file", metavar = "filename", default = "wharfy.json", help = "Configuration file to use. Defaults to %(default)s.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be given multiple times.")
	mc.register("start", "Start some Wharfy containers", genparser, action = ActionStart)

	def genparser(parser):
		parser.add_argument("-c", "--config-file", metavar = "filename", default = "wharfy.json", help = "Configuration file to use. Defaults to %(default)s.")
		parser.add_argument("-f", "--forward-ports", action = "store_true", help = "By default, a console does not do port forwarding. This option enables forwarding of ports.")
		parser.add_argument("-p", "--process", metavar = "filename", default = "/bin/bash", help = "Process to start for console interaction. Defaults to %(default)s.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be given multiple times.")
	mc.register("console", "Start a Wharfy container console", genparser, action = ActionConsole)

	return mc.run(argv[1:])

if __name__ == "__main__":
	sys.exit(main(sys.argv))
