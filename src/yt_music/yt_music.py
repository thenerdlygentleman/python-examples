import logging

from python.src.utils.driver import Driver

logger = logging.getLogger(__name__)


class YoutubeMusic:
	"""Create a Youtube music client with selenium."""

	def __init__(self) -> None:
		"""Create a webdriver instance."""
		ytm_driver = Driver()
		ytm_driver.create(headless=False)
		logger.debug("Youtube music driver created.")
