import logging
from pathlib import Path

import cv2 as cv
import numpy as np

logger = logging.getLogger(__name__)


class ImageOpenCV:
	"""Edit images with OpenCV."""

	def __init__(self, image_path: str) -> None:
		"""Load an image."""
		self.image_path = Path(image_path)
		self.image = cv.imread(filename=self.image_path)

		logger.debug("Open image: %s", self.image)

	def resize_image(
		self,
		width: int,
		height: int,
	) -> None:
		"""Resize the image."""
		self.image_resized = cv.resize(
			src=self.image,
			dsize=[width, height],
			interpolation=cv.INTER_LINEAR,
		)

		logger.debug("Resized image %s to [%s, %s]", self.image_path, width, height)

		return self.image_resized

	def convert_to_grayscale(self) -> None:
		"""Convert the image to grayscale."""
		self.image_grey = cv.cvtColor(src=self.image, code=cv.COLOR_BGR2GRAY)

		logger.debug("Converted %s to greyscale", self.image_path)

		return self.image_grey

	@classmethod
	def compare_images(
		cls,
		*args: bytes,
		output_image_path: str,
		accepted_error_rate: int,
	) -> bool:
		"""Compare two images with each other."""
		height, width = args[0].shape
		difference = cv.subtract(*args)
		error = np.sum(a=difference**2)

		image_difference = error / (float(height * width))
		image_difference_corrected = float(round(image_difference, 2))

		if image_difference_corrected > 100:
			image_difference_corrected = 100

		file_path = Path(output_image_path)

		cv.imwrite(filename=file_path, img=difference)

		if 0 <= image_difference <= accepted_error_rate:
			logger.debug(
				"Difference is accepted (difference = %s | accepted_error_rate = %s)",
				image_difference_corrected,
				accepted_error_rate,
			)
			return True

		logger.error(
			"Difference is not accepted (difference = %s | accepted_error_rate = %s)",
			image_difference_corrected,
			accepted_error_rate,
		)
		return False
