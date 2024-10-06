import logging
import os
import subprocess
import sys
import time

logger = logging.getLogger(__name__)


class Shell:
	"""Run shell commands via python."""

	def __init__(self, root: bool = False) -> None:
		"""Set if the shell should be run with root or not.

		if `root` is `True` the commands will
		be executed as root user (if logged in as root) or with sudo.

		Arguments:
		---------
			root: True

		Returns:
		-------
			`None`

		"""
		self.root = root

		if self.root:
			if os.geteuid() == 0:
				self.permission = ""
				logger.debug(msg="Command will be executed as root")
			else:
				self.permission = "sudo "
				logger.debug(msg="Commands will be executed with 'sudo'")
		else:
			self.permission = ""

	def execute_command(
		self, command: str, timeout: int = 30
	) -> tuple[list[str], list[str]]:
		"""Execute a command in the shell.

		`timeout` can be used to adjust the time a command should take.

		Arguments:
		---------
			command: whoami
			timeout: 30

		Returns:
		-------
			`tuple` of two `lists` that contains `strings`

		"""
		command = self.permission + command

		command = command.split()

		output = subprocess.run(
			args=command, capture_output=True, check=False, timeout=timeout
		)
		stdout = output.stdout.decode(encoding="utf-8").splitlines()
		stderr = output.stderr.decode(encoding="utf-8").splitlines()

		if stdout != []:
			logger.info("stdout = %s", stdout)
		if stderr != []:
			logger.error("stderr = %s", stderr)

		return stdout, stderr

	@classmethod
	def check_service_status(cls, service_name: str, tries: int = 10) -> None:
		"""Checks if the systemd service `service_name` is running.

		If the service is not starting up after `tries` tries,
		the script is ending.
		"""
		count = 0

		while count < tries:
			if os.system(f"systemctl is-active --quiet {service_name}") == 0:  # noqa: S605
				logger.info("%s is active and running", service_name)
				return

			count += 1
			time.sleep(2)

		message = f"{service_name} could not be started"
		logger.error(message)
		sys.exit(message)
