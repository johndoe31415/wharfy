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

import os
import subprocess
from .MultiCommand import LoggingAction
from .WorkDir import WorkDir
from .Configfile import Configfile

class ActionBuild(LoggingAction):
	def _run_build_script(self, container, arg: str):
		if container.build_script is not None:
			build_script = self._config.path(container.build_script)
			with WorkDir(os.path.dirname(build_script)):
				subprocess.run([ build_script, arg ], check = True)

	def run(self):
		self._config = Configfile(self._args.config_file)
		for container in self._config.containers:
			try:
				self._run_build_script(container, "setup")

				cmd = [ "docker", "buildx", "build" ]
				cmd += [ "--tag", container.name ]
				cmd += [ "--file", "Dockerfile" ]
				cmd += [ self._config.path(container.build_directory) ]
				subprocess.run(cmd, check = True)

			finally:
				self._run_build_script(container, "clean")
