import logging

import paramiko

logger = logging.getLogger(__name__)


class SSH:
	"""Python API for SSH interactions."""

	def __init__(self, user: str, hostname: str, key_file: str) -> None:
		"""Init."""
		self.ssh = paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.private_key = paramiko.Ed25519Key.from_private_key_file(key_file)
		self.hostname = hostname
		self.user = user

	def _connect_to_host(self) -> None:
		"""Connect to the remote host."""
		self.ssh.connect(
			hostname=self.hostname, username=self.user, pkey=self.private_key
		)
		logger.debug("Connected to host: %s", self.hostname)

	def execute_command(self, command: str) -> None:
		"""Execute a command on the remote host."""
		self._connect_to_host()

		stdin, stdout, stderr = self.ssh.exec_command(command=command)
		stdout = stdout.read().decode().splitlines()
		stderr = stderr.read().decode().splitlines()

		logger.debug("Executed SSH command: %s", command)
		if stdout != []:
			logger.info("stdout = %s", stdout)
		if stderr != []:
			logger.error("stderr = %s", stderr)

		self._close_connection()

	def _close_connection(self) -> None:
		"""Closes the connection to the remote host."""
		self.ssh.close()
		logger.debug("Closed connection to %s", self.hostname)
