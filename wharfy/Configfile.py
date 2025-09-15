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
import json
import contextlib

class ContainerConfigfile():
	def __init__(self, config: "Configfile", container: dict):
		self._config = config
		self._container = container

	@property
	def name(self):
		return self._container["name"]

	@property
	def env(self):
		return self._container.get("env", { })

	@property
	def network(self):
		return self._container.get("network", { })

	@property
	def network_type(self):
		return self.network.get("type")

	@property
	def network_forwardings(self):
		return self.network.get("forward", [ ])

	@property
	def build(self):
		return self._container.get("build", { })

	@property
	def build_directory(self):
		return self.build.get("directory")

	@property
	def build_script(self):
		return self.build.get("setup_script")

	@property
	def volumes(self):
		return self._container.get("volumes", { }).items()

	@property
	def cmd(self):
		return self._container.get("cmd")

	@property
	def docker_network_args(self):
		match self.network_type:
			case "bridge":
				return [ "--network=bridge", "--add-host=host.docker.internal:host-gateway" ]

			case None:
				return [ ]

			case "_":
				raise ValueError(f"Unknown network type: {self.network_type}")

	@property
	def docker_forwarding_args(self):
		args = [ ]
		for forwarding in self.network_forwardings:
			args += [ "-p", forwarding ]
		return args

	@property
	def docker_volume_args(self):
		args = [ ]
		for (mntpoint, mntargs) in self.volumes:
			args += [ "-v", f"{self._config.directory(mntargs['src'])}:{mntpoint}" ]
		return args

	@property
	def docker_environment_args(self):
		args = [ ]
		for (key, value) in self.env.items():
			args += [ "-e", f"{key}={value}" ]
		return args



class Configfile():
	def __init__(self, filename: str):
		self._base_path = os.path.realpath(os.path.dirname(filename))
		with open(filename) as f:
			self._config = json.load(f)

	@property
	def containers(self):
		return iter(ContainerConfigfile(self, container) for container in self._config["containers"])

	def path(self, path: str):
		if path.startswith("/"):
			# Absolute
			return path
		elif path.startswith("~"):
			# Home-relative
			return os.path.expanduser(path)
		else:
			# Relative
			return os.path.realpath(f"{self._base_path}/{path}")

	def directory(self, path: str):
		path = self.path(path)
		with contextlib.suppress(FileExistsError):
			os.makedirs(path)
		return path
