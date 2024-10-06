import logging
import time
from pathlib import Path

import yaml
from evdev import ecodes as e, UInput

logger = logging.getLogger(__name__)

# Global variables
# ============================================================================ #
BUTTON_SLEEP = 0.1
# ============================================================================ #


class EventDevice:
	"""Controll evdev devices."""

	def __init__(self) -> None:

		self.keyboard = UInput()
		self.touchscreen = UInput.from_device("/dev/input/event0", name="touchscreen")

		logger.debug("Touchscreen and keyboard created.")

	def create_from_device(self, *device_path: str, device_name: str) -> None:
		"""Create a event device from another device."""
		self.eventdevice = UInput.from_device(*device_path, name=device_name)

		logger.debug("Created %s from device: %s", device_name, *device_path)

	def touchscreen_event(
		self,
		btn_touch: int,
		mt_slot: int,
		tracking_id: int,
		x_absolute: float,
		y_absolute: float,
	) -> None:
		"""Basic touchscreen event."""
		self.touchscreen.write(e.EV_KEY, e.BTN_TOUCH, btn_touch)
		self.touchscreen.write(e.EV_ABS, e.ABS_MT_SLOT, mt_slot)
		self.touchscreen.write(e.EV_ABS, e.ABS_MT_TRACKING_ID, tracking_id)
		self.touchscreen.write(e.EV_ABS, e.ABS_MT_POSITION_X, x_absolute)
		self.touchscreen.write(e.EV_ABS, e.ABS_MT_POSITION_Y, y_absolute)
		self.touchscreen.write(e.EV_ABS, e.ABS_X, x_absolute)
		self.touchscreen.write(e.EV_ABS, e.ABS_Y, y_absolute)
		self.touchscreen.syn()
		time.sleep(BUTTON_SLEEP)

		logger.debug("Touchscreen event at [%s, %s]", x_absolute, y_absolute)

	def touchscreen_drag_drop(
		self,
		x_start: int,
		y_start: int,
		x_end: int,
		y_end: int,
	) -> None:
		"""Perform a touchscreen drag and drop action."""
		self.touchscreen_event(
			btn_touch=1,
			mt_slot=0,
			tracking_id=1,
			x_absolute=x_start,
			y_absolute=y_start,
		)

		steps = 1

		if x_start == x_end:
			x_multiplicator = 0
		elif x_start < x_end:
			x_multiplicator = 1
		else:
			x_multiplicator = -1

		if y_start == y_end:
			y_multiplicator = 0
		elif y_start < y_end:
			y_multiplicator = 1
		else:
			y_multiplicator = -1

		x_range = abs(x_start - x_end)
		y_range = abs(y_start - y_end)

		maximum_range = x_range if x_range == y_range or x_range > y_range else y_range

		x_position = x_start
		y_position = y_start

		for _ in range(maximum_range):
			if x_end == x_position:
				pass
			else:
				x_position = x_position + (steps * x_multiplicator)
			if y_end == y_position:
				pass
			else:
				y_position = y_position + (steps * y_multiplicator)

			self.touchscreen.write(e.EV_ABS, e.ABS_MT_POSITION_X, x_position)
			self.touchscreen.write(e.EV_ABS, e.ABS_MT_POSITION_Y, y_position)
			self.touchscreen.write(e.EV_ABS, e.ABS_X, x_position)
			self.touchscreen.write(e.EV_ABS, e.ABS_Y, y_position)
			self.touchscreen.syn()
			time.sleep(0.0001)

		self.touchscreen_event(
			btn_touch=0,
			mt_slot=-1,
			tracking_id=-1,
			x_absolute=x_end,
			y_absolute=y_end,
		)

		logger.debug(
			"Drag and drop from [%s, %s] to [%s, %s]", x_start, y_start, x_end, y_end
		)

	def touchscreen_press(
		self,
		x_position: int,
		y_position: int,
		hold_duration: float = 0,
	) -> None:
		"""Perform a touchscreen press action."""
		self.touchscreen_event(
			btn_touch=1,
			mt_slot=0,
			tracking_id=1,
			x_absolute=x_position,
			y_absolute=y_position,
		)

		if hold_duration != 0:
			logger.debug("Hold touchscreen at [%s, %s]", x_position, y_position)

			time.sleep(hold_duration)

			logger.debug(
				"Release touchscreen at [%s, %s] after %s seconds",
				x_position,
				y_position,
				hold_duration,
			)

		self.touchscreen_event(
			btn_touch=0,
			mt_slot=-1,
			tracking_id=-1,
			x_absolute=x_position,
			y_absolute=y_position,
		)

		logger.debug("Touchscreen pressed at [%s, %s]", x_position, y_position)

	def keyboard_press(self, key_name: str) -> None:
		"""Press a keyboard key."""
		key = key_name.upper()

		key = getattr(e, f"KEY_{key}")

		try:
			self.keyboard.write(e.EV_KEY, key, 1)
			self.keyboard.write(e.EV_KEY, key, 0)
			self.keyboard.syn()

			logger.debug("Keyboard pressed key: %s", key_name)

		except:  # noqa: E722
			logger.error("Key %s cannot be pressed on Keyboard", key_name)  # noqa: TRY400

	def keyboard_press_multiple_keys(self, *args: str) -> None:
		"""Press multiple keyboard keys at the same time."""
		key_list_message = []

		for key in args:
			if key == " ":
				key = "SPACE"  # noqa: PLW2901

			key = key.upper()  # noqa: PLW2901

			try:
				key_code = f"KEY_{key}"

				key_code = getattr(e, key_code)

				self.keyboard.write(e.EV_KEY, key_code, 1)

				key_list_message.append(key)

			except:  # noqa: E722
				logger.error("Key %s cannot be pressed on keyboard", key)  # noqa:TRY400

		for key in key_list_message:
			key = f"KEY_{key}"  # noqa: PLW2901

			key = getattr(e, key)  # noqa: PLW2901

			self.keyboard.write(e.EV_KEY, key, 0)

		self.keyboard.syn()

		logger.debug("Keyboard pressed keys: %s", args)

	def keyboard_write_string(self, string: str) -> None:
		"""Press a string with the keyboard."""
		new_string = ""

		for letter in string:
			new_letter = letter

			try:
				if new_letter == " ":
					new_letter = "SPACE"

				self.keyboard_press(key_name=new_letter)

				new_string = new_string + letter

			except:  # noqa:E722
				logger.error("Key %s cannot be pressed on keyboard", letter)  # noqa: TRY400

		logger.debug("Keyboard wrote keys in: %s", new_string)

	def close(self) -> None:
		"""Close the event devices."""
		self.touchscreen.close()
		self.keyboard.close()

		logger.debug("All devices are closed.")
