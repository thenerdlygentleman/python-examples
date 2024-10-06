import logging
from pathlib import Path

from PIL import Image
from src.system.files import Files

logger = logging.getLogger(__name__)


class ImageEXIF:
	"""Class for retrieving meta data from images and editing them."""

	def __init__(self, image_path: str) -> None:
		"""Takes the input image and returns the image data.

		Arguments:
		---------
			image_path: /path/to/image.png

		Returns:
		-------
			`Image` object

		"""
		self.image_path = Path(image_path)
		self.image = Image.open(fp=self.image_path)

		logger.debug("Open %s: %s", self.image_path, self.image)

	def get_format(self) -> str:
		"""Retrieve the format of the image file.

		Arguments:
		---------
			None

		Returns:
		-------
			`string` of the image format

		"""
		self.format = self.image.format

		logger.debug("Format of %s: %s", self.image_path, self.format)

		return self.format

	def get_exif(self) -> dict:
		"""Get the exif data, from the image.

		Arguments:
		---------
			None

		Returns:
		-------
			`dict` of exif data

		"""
		self.exif = self.image._getexif()

		if self.exif is None:
			logger.error("%s has no exif data", self.image_path)
		else:
			logger.debug("Extracted exif data of %s", self.image_path)

		return self.exif

	def get_timestamp(self) -> str:
		"""Get the timestamp of the image.

		Arguments:
		---------
			None

		Returns:
		-------
			`string` of timestamp

		"""
		if hasattr(self, "exif"):
			pass
		else:
			self.exif = self.get_exif()

		if self.exif is None:
			logger.error("%s has no exif data and no timestamp", self.image_path)
		else:
			self.timestamp = self.exif[36867].replace(":", "").replace(" ", "_")
			logger.debug("Date of %s: %s", self.image_path, self.timestamp)

		return self.timestamp

	def rename_image_with_timestamp(self) -> None:
		"""Renames the image with the timestamp.

		Arguments:
		---------
			None

		Returns:
		-------
			`Path` object of the renamed image

		"""
		if hasattr(self, "timestamp"):
			pass
		else:
			self.exif = self.get_exif()
			self.timestamp = self.get_timestamp()

		if self.timestamp is None:
			logger.error("%s has no timestamp and cannot be renamed", self.image_path)

		image_path = self.image_path

		self.image_path = Files.rename_file(
			file_path=self.image_path,
			new_name=self.timestamp,
			autorun=True,
		)

		logger.debug(
			"%s renamed after with timestamp %s | new image path %s",
			image_path,
			self.timestamp,
			self.image_path,
		)

		return self.image_path
