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

import subprocess
from .MultiCommand import LoggingAction
from .Configfile import Configfile

class ActionStart(LoggingAction):
	def run(self):
		self._config = Configfile(self._args.config_file)
		for container in self._config.containers:
			if self._args.remove_container:
				subprocess.run([ "docker", "rm", container.name ], check = False, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

			cmd = [ "docker", "run" ]
			if self._args.foreground:
				cmd += [ "--tty" ]
			else:
				cmd += [ "--detach=true", "--restart", "unless-stopped" ]
			cmd += [ "--name", container.name ]
			cmd += container.docker_network_args + container.docker_forwarding_args + container.docker_volume_args + container.docker_environment_args
			cmd += [ container.name ]
			if container.cmd is not None:
				cmd += [ container.cmd ]
			subprocess.run(cmd, check = True)
