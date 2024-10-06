import os  # noqa: INP001
import sys
from pathlib import Path

import pytest

RESOURCES_DIRECTORY_PATH = Path(__file__).parent

def check_if_linux() -> bool:
	"""Check if the platform is linux or not."""
	if sys.platform == "linux":
		return False
	return True


def check_if_root() -> bool:
	"""Check if the tests are executed as root."""
	if os.geteuid() == 0:
		return False
	return True


only_on_linux = pytest.mark.skipif(check_if_linux(), reason="Can only be run on Linux")
only_as_root = pytest.mark.skipif(check_if_root(), reason="Can only be run as root")
only_as_user = pytest.mark.skipif(
	not check_if_root(), reason="Can only be run as non-root "
)


@pytest.fixture()
def test_directory() -> Path:
	"""Returns the absolute path of the test_directory."""
	return RESOURCES_DIRECTORY_PATH


@pytest.fixture()
def image_dict() -> dict:
	"""Returns a dictionary with the test image files."""
	return {
		"image_1": {"path": Path(f"{RESOURCES_DIRECTORY_PATH}/image_1.jpg"), "format": "JPEG"},
		"image_2": {"path": Path(f"{RESOURCES_DIRECTORY_PATH}/image_2.png"), "format": "PNG"},
		"image_3": {"path": Path(f"{RESOURCES_DIRECTORY_PATH}/image_3.bmp"), "format": "BMP"},
		"image_4": {"path": Path(f"{RESOURCES_DIRECTORY_PATH}/image_4.gif"), "format": "GIF"},
		"image_5": {"path": Path(f"{RESOURCES_DIRECTORY_PATH}/image_1.tiff"), "format": "tiff"},
		"image_6": {
			"path": Path(f"{RESOURCES_DIRECTORY_PATH}/image_6.jpg"),
			"format": "JPEG",
			"timestamp": "20090323_140323",
		},
	}
