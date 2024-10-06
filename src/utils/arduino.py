import logging

import serial

logger = logging.getLogger(__name__)


class Arduino:
	"""Python API for Arduino boards."""

	def __init__(self, port_name: str, baud_rate: int) -> None:
		"""Opens a serial port.

		Arguments:
		---------
			port_name: /dev/ttyACM0
			baud_rate: 9600

		Returns:
		-------
			`None`

		"""
		if port_name is None:
			logger.error("No serial port was given.")
		else:
			self.serial_port = serial.Serial(port=port_name, baudrate=baud_rate)
			logger.debug("Serial port: %s", self.serial_port)

	def output_from_port(self) -> str:
		"""Reads the output of the serial port and returns it."""
		serial_port_output = (
			self.serial_port.readline().decode(encoding="utf-8").strip()
		)
		if hasattr(self, "serial_port"):
			logger.debug("Serial port output: %s", serial_port_output)
		return serial_port_output
