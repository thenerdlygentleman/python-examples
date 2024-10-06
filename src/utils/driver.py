import datetime
import logging
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


class Driver:
	"""Control a web driver with python and selenium."""

	def create(
		self,
		profile_file: str,
		access_to_mic_camera: bool = True,
		headless: bool = True,
		initial_height: int = 720,
		initial_width: int = 1280,
	) -> webdriver:
		"""Creates a webdriver instance.

		Its possible to launch the webdriver in headless mode if
		`headless` is `True`.

		Arguments:
		---------
			profile_file: path/to/profile_file
			access_to_mic_camera: True
			headless: True
			initial_height: 720
			initial_width: 1280

		Returns:
		-------
			`webdriver`

		"""
		options = Options()
		options.add_argument("--no-sandbox")
		options.add_argument("--disable-gpu")
		options.add_argument(f"--window-size={initial_width},{initial_height}")

		if access_to_mic_camera:
			options.add_experimental_option(
				"prefs",
				{
					"profile.default_content_setting_values.media_stream_mic": 1,
					"profile.default_content_setting_values.media_stream_camera": 1,
				},
			)
		logger.debug("Access to microphone and camera: %s", access_to_mic_camera)

		if headless:
			options.add_argument("--headless")
		logger.debug("Headless status: %s", headless)

		if profile_file is not None:
			options.add_argument(f"user-data-dir={Path(profile_file)}")
			logger.debug("Open browser with profile: %s", profile_file)

		self.driver = webdriver.Chrome(options=options)

		if self.driver is None:
			logger.error("Driver was not created.")
		else:
			logger.info("Driver was created.")

		return self.driver

	def position_driver(
		self,
		height: int,
		width: int,
		x_position: int,
		y_position: int,
	) -> None:
		"""Positions and resizes the webdriver.

		Arguments:
		---------
			height: 720
			width: 1280
			x_position: 50
			y_position: 50

		Returns:
		-------
			`None`

		"""
		self.driver.set_window_position(x=x_position, y=y_position)
		self.driver.set_window_size(width=width, height=height)

		logger.debug(
			"Driver positioned: [%s x %s] | [%s, %s]",
			height,
			width,
			x_position,
			y_position,
		)

	def get_current_window_handler(self) -> str:
		"""Returns the current window handler."""
		window_handler = self.driver.current_window_handle

		logger.debug("Current window handler: %s", window_handler)

		return window_handler

	def open_new_tab(self) -> str:
		"""Open a new tab."""
		self.driver.switch_to.new_window(type_hint="tab")

		handler = self.get_current_window_handler()

		logger.debug("Open new tab with window handler: %s", handler)

		return handler

	def get_all_window_handler(self) -> list[str]:
		"""Returns a list of all active window handlers."""
		all_handler = self.driver.window_handles

		logger.debug("Active window handlers: %s", all_handler)

		return all_handler

	def switch_to_tab(self, window_handler: str) -> None:
		"""Switch to given window handler."""
		current_handler = self.get_current_window_handler()

		if current_handler == window_handler:
			logger.error(
				"Already on desired window handler: %s is %s",
				current_handler,
				window_handler,
			)
		else:
			self.driver.switch_to.window(window_name=window_handler)
			new_current_handler = self.get_current_window_handler()
			if new_current_handler == window_handler:
				logger.debug("Switched from %s to %s", current_handler, window_handler)
			else:
				logger.error(
					"Did not switch to new window handler, current handler: %s",
					new_current_handler,
				)

	def refresh_page(self) -> None:
		"""Refresh the current window."""
		self.driver.refresh()

		logger.debug("Page %s was refreshed", self.get_current_url())

	def open_webpage(self, url: str) -> None:
		"""Open webpage."""
		self.driver.get(url=url)

		logger.debug("Open page: %s", url)

	def get_current_url(self) -> str:
		"""Returns the current url."""
		url = self.driver.current_url

		logger.debug("Current url: %s", url)

		return url

	def find_element_on_page(self, element: str) -> None:
		"""Find element on page."""
		found_element = self.driver.find_element(by=By.CSS_SELECTOR, value=element)

		logger.debug("Found element: %s", element)

		return found_element

	def click_element(self, element: str) -> None:
		"""Click desired element."""
		click_element = self.find_element_on_page(element=element)

		click_element.click()

		logger.debug("Clicked element: %s", click_element)

	def input_string(self, element: str, input_string: str) -> None:
		"""Input a string in element."""
		input_element = self.find_element_on_page(element=element)

		input_element.send_keys(input_string)

		logger.debug("Input %s to element %s", input_string, input_element)

	def get_size_of_element(self, element: str) -> dict:
		"""Returns the size of an webelement."""
		size = self.driver.find_element(by=By.CSS_SELECTOR, value=element).rect
		# output: {'height': 0, 'width': 0, 'x': 0, 'y': 0}

		logger.debug("Size of webelement %s: %s", element, size)

		return size

	def drag_and_drop(self, x_start: int, y_start: int, x_end: int, y_end: int) -> None:
		"""Drag and drop from point A to B."""
		body = self.find_element_on_page(element="body")

		size_of_body = self.get_size_of_element(element="body")

		# the origin point of the element is in the center => change to the upper left corner

		x_0 = size_of_body["x"] - size_of_body["height"] / 2

		y_0 = size_of_body["y"] - size_of_body["width"] / 2

		logger.debug("New origin of body: [%s, %s]", x_0, y_0)

		x_a = x_0 + x_start
		y_a = y_0 + y_start

		x_b = x_0 + x_end
		y_b = y_0 + y_end

		action = ActionChains(driver=self.driver)

		action.move_to_element_with_offset(to_element=body, xoffset=x_a, yoffset=y_a)

		action.click_and_hold()

		action.move_to_element_with_offset(to_element=body, xoffset=x_b, yoffset=y_b)

		action.release()

		action.perform()

		logger.debug(
			"Drag and drop was successful from [%s, %s] to [%s, %s]",
			x_a,
			y_a,
			x_b,
			y_b,
		)

	def make_screenshot(self, screenshot_name: str, screenshot_directory: str) -> Path:
		"""Make a screenshot."""
		time_stamp = datetime.datetime.now(tz=datetime.timezone.utc).strftime(
			"%Y%m%d_%H%M%S"
		)

		image_name = Path(f"{screenshot_directory}/{screenshot_name}_{time_stamp}.png")

		self.driver.save_screenshot(filename=image_name)

		logger.debug("Screenshot saved under: %s", image_name)

		return image_name

	def close(self) -> None:
		"""Close the webdriver."""
		self.driver.close()

		logger.debug("Webdriver closed: %s", self.driver)
