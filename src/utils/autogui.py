import datetime
import logging
from pathlib import Path

import pyautogui as pag

from constants import TMP_PATH

logger = logging.getLogger(__name__)


class AutoGui:
	"""Perform GUI actions."""

	def __init__(self) -> None:
		"""Get screen and cursor information."""
		self.screen_size = {}
		self.cursor_position = {}

	def make_screenshot(self, screenshot_directory: str = TMP_PATH) -> Path:
		"""Perform a screenshot.

		Arguments:
		---------
			screenshot_directory: /path/to/screenshot

		Returns:
		-------
			`Path` of screenshot

		"""
		timestamp = datetime.datetime.now(tz=datetime.timezone.utc).strftime(
			"%Y%m%d_%H%M%S_"
		)

		screenshot_path = Path(f"{screenshot_directory}/{timestamp}.png")

		pag.screenshot(imageFilename=screenshot_path)

		logger.debug("Screenshot saved under: %s", screenshot_path)

		return screenshot_path

	def get_screen_size(self) -> dict:
		"""Get the current screen size.

		Arguments:
		---------
			None

		Returns:
		-------
			`dict` with screen size

		"""
		self.screen_size["width"], self.screen_size["height"] = pag.size()

		logger.debug("Screen size is: %s", self.screen_size)

		return self.screen_size

	def get_cursor_position(self) -> dict:
		"""Get the current cursor position.

		Arguments:
		---------
			None

		Returns:
		-------
			`dict` with cursor position

		"""
		self.cursor_position["x_position"], self.cursor_position["y_position"] = (
			pag.position()
		)

		logger.debug("Cursor position: %s", self.cursor_position)

		return self.cursor_position

	def move_cursor(self, x_position: int, y_position: int) -> None:
		"""Move the cursor to a desired position.

		Arguments:
		---------
			x_position: 50
			y_position: 50

		Returns:
		-------
			`bool` if the cursor was moved correctly

		"""
		pag.moveTo(x=x_position, y=y_position)
		is_position = self.get_cursor_position()
		new_position = {"x_position": x_position, "y_position": y_position}

		if new_position == self.cursor_position:
			logger.debug("Cursor was moved successfully: %s", new_position)
		else:
			logger.error(
				"Cursor was not moved successfully: %s is not %s",
				new_position,
				is_position,
			)

	def click_cursor(self, x_position: int, y_position: int, button: str) -> None:
		"""Perform a click action at desired position.

		Arguments:
		---------
			x_position: 50
			y_position: 50
			button: RIGHT

		Returns:
		-------
			`None`

		"""
		pag.click(x=x_position, y=y_position, button=button)

		logger.debug(
			"Performed click action with %s at [%s, %s]", button, x_position, y_position
		)
