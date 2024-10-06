from pathlib import Path

from PIL import Image
from src.system.files import Files
from src.images.imageexif import ImageEXIF


def test_open_image(image_dict: dict) -> None:
	"""Test if a image can be opened."""
	image_test = ImageEXIF(image_path=image_dict["image_6"]["path"])
	assert image_test is not None


def test_get_format_jpeg(image_dict: dict) -> None:
	"""Test if the JPEG format can be retrieved."""
	format_test = ImageEXIF(image_path=image_dict["image_6"]["path"]).get_format()
	assert format_test == image_dict["image_6"]["format"]


def test_get_format_png(image_dict: dict) -> None:
	"""Test if the PNG format can be retrieved."""
	format_test = ImageEXIF(image_path=image_dict["image_2"]["path"]).get_format()
	assert format_test == "PNG"


def test_get_format_bmp(image_dict: dict) -> None:
	"""Test if the BMP format can be retrieved."""
	format_test = ImageEXIF(image_path=image_dict["image_3"]["path"]).get_format()
	assert format_test == "BMP"


def test_get_exif(image_dict: dict) -> None:
	"""Test if the exif data can be retrieved."""
	exif_reference = Image.open(fp=image_dict["image_6"]["path"])._getexif()
	exif_test = ImageEXIF(image_path=image_dict["image_6"]["path"]).get_exif()
	assert exif_reference == exif_test


def test_get_timestamp(image_dict: dict) -> None:
	"""Test if the timestamp of a image can be retrieved."""
	timestamp_test = ImageEXIF(image_path=image_dict["image_6"]["path"]).get_timestamp()
	assert timestamp_test == image_dict["image_6"]["timestamp"]


def test_rename_image_with_date(image_dict: dict, tmp_path: Path) -> None:
	"""Test if a image can be renamed with its timestamp."""
	image_6_copy = Files.copy_file(image_dict["image_6"]["path"], destination=tmp_path)
	renamed_image_1 = ImageEXIF(image_path=image_6_copy).rename_image_with_timestamp()
	renamed_image_2 = Files.get_content_of_directory(directory_path=tmp_path)
	assert renamed_image_1 == Path(
		f'{tmp_path}/{image_dict["image_6"]["timestamp"]}.jpg',
	)
	assert renamed_image_2[0] == Path(
		f'{tmp_path}/{image_dict["image_6"]["timestamp"]}.jpg',
	)
