from __future__ import annotations

import datetime
import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


class Files:
	"""Class to play around with files and directories."""

	@classmethod
	def get_content_of_directory(
		cls,
		directory_path: str,
		search_name: str | None = None,
	) -> list[Path]:
		"""Get all the content in a directory.

		If there is no `search_name` given, all items in the `directory_path` are returned.

		Arguments:
		---------
			directory_path: /path/to/director
			search_name: file_name

		Returns:
		-------
			`list` with `path` object of the content in `directory_path`

		"""
		directory_path = Path(directory_path)
		directory_content_list = []

		search_name = "*" if search_name is None else f"*{search_name}*"

		directory_content = directory_path.glob(search_name)
		for item in directory_content:
			directory_content_list.append(item)
		directory_content_list.sort()

		logger.debug(
			"Found %s items with %s in %s: %s",
			len(directory_content_list),
			search_name,
			directory_path,
			directory_content_list,
		)

		return directory_content_list

	@classmethod
	def get_files_in_directory_tree(cls, directory_path: str) -> list[Path]:
		"""Get all files in a directory tree.

		Arguments:
		---------
			directory_path: /path/to/directory

		Returns:
		-------
			`list` of `path` objects from the files in `directory_path`

		"""
		# directory_content = Path(directory_path).glob("**/*")
		directory_content = cls.get_content_of_directory(
			directory_path=directory_path,
			search_name="*/",
		)
		directory_content_list = [item for item in directory_content if item.is_file()]

		logger.debug(
			"Found %s files in %s: %s",
			len(directory_content_list),
			directory_path,
			directory_content_list,
		)

		return directory_content_list

	@classmethod
	def create_file(cls, *file_path: str) -> list[Path] | Path:
		"""Create multiple files.

		Arguments:
		---------
			*file_path: /path/to/file.txt

		Returns:
		-------
			`list` with `Path` object (returns only `Path` object if only one
			file was created)

		"""
		content = []

		for file in file_path:
			file_path = Path(file)

			with Path.open(file_path, "x"):
				pass

			file_created = Path(file_path).is_file()

			if file_created:
				content.append(file_path)
				logger.debug("Files created: %s", file_path)
			else:
				logger.error("File was not created: %s", file_path)

		return content[0] if len(content) == 1 else content

	@classmethod
	def copy_file(
		cls,
		*file_path: str,
		destination: str | None = None,
	) -> list[Path] | Path:
		"""Copy multiple files to one directory.

		Arguments:
		---------
			*file_path: /path/to/old/file.txt
			destination: /path/to/new

		Returns:
		-------
			`list` of `Path` objects (returns only a `Path` object) if only one
			file is copied.

		"""
		content = []

		for item in file_path:
			file = Path(item)
			file_name = file.name
			# file_parent = file.parent

			if file.is_file():
				logger.debug("%s exits", file)
			else:
				logger.error("%s does not exits", file)
				continue

			destination_path = f"{destination}/{file_name}"
			destination_path = Path(destination_path)

			if destination_path.exists():
				logger.error("%s already exits in %s", file, destination)
			else:
				try:
					shutil.copy(file, destination_path)
					content.append(destination_path)
					logger.debug("Copy file: %s --> %s", file, destination_path)
				finally:
					logger.error("Could not copy: %s --> %s", file, destination_path)

		return content[0] if len(content) == 1 else content

	@classmethod
	def rename_file(
		cls,
		file_path: str | None = None,
		new_name: str | None = None,
		autorun: bool = False,
	) -> Path:
		"""Rename a file.

		Arguments:
		---------
			file_path: /path/to/file.txt
			new_name: new_name
			autorun: True

		Returns:
		-------
			`path` object of the renamed file.

		"""
		file_path = Path(file_path)
		parent = file_path.parent
		old_name = file_path.stem
		suffix = file_path.suffix

		new_name = new_name if autorun else input("Enter new name for %s: ", old_name)

		logger.debug("New name for %s: %s | Autorun: %s", file_path, new_name, autorun)

		tmp_name = new_name
		count = 1

		while Path(f"{parent}/{new_name}{suffix}").exists():
			new_name = f"{tmp_name}_{count}"
			count += 1

		source = f"{parent}/{old_name}{suffix}"
		destination = f"{parent}/{new_name}{suffix}"

		renamed_file = Path(source)
		renamed_file.rename(destination)

		destination_path = Path(destination)

		logger.debug("Renamed file: %s --> %s", source, destination)

		return destination_path

	@classmethod
	def remove_file(cls, *file_path: str) -> None:
		"""Remove multiple files.

		Arguments:
		---------
			*file_path: /path/to/file.txt

		Returns:
		-------
			None

		"""
		for item in file_path:
			file = Path(item)

			if file.is_file():
				file.unlink()

				logger.debug("Removed file %s", file)
			else:
				logger.error("%s is not a file and cannot be removed", file)

	@classmethod
	def generate_configuration_file(
		cls,
		configuration_path: Path,
		configuration_dict: dict,
	) -> Path:
		"""Generate a configuration file."""
		configuration_path = Path(configuration_path)

		if configuration_path.exists():
			configuration_path.unlink()
		for key, value in configuration_dict.items():
			with Path.open(configuration_path, "a") as configuration_file:
				configuration_file.write(f"{key}={value}\n")

		with Path.open(configuration_path) as configuration_file:
			if configuration_file != "":
				logger.debug("Generated %s", configuration_path)
			else:
				logger.error("Generated %s is empty", configuration_path)

	@classmethod
	def create_directory(
		cls,
		*directory_path: str,
	) -> list[Path] | Path:
		"""Create multiple directories.

		Arguments:
		---------
			*directory_path: /path/to/directory_parent

		Returns:
		-------
			`list` contains `path` object (returns only `path` object if only
			one directory is created)

		"""
		content = []

		for directory in directory_path:
			new_directory = Path(directory)

			if new_directory.exists():
				logger.error("%s already exits and cannot be created", directory)

			else:
				new_directory.mkdir()
				content.append(new_directory)
				logger.debug("Directory %s created", directory)

		if len(content) == 1:
			return content[0]
		return new_directory

	@classmethod
	def create_time_directory(
		cls,
		directory_path: str | None = None,
	) -> Path:
		"""Create a directory with the timestamp as a name.

		Arguments:
		---------
			directory_path: /path/to/directory_parent

		Returns:
		-------
			`path` object with the syntax '/path/to/test_directoy_YYYYMMDD_HHMMSS'

		"""
		time_stamp = datetime.datetime.now(tz=datetime.timezone.utc).strftime(
			"%Y%m%d_%H%M%S"
		)
		directory_path = f"{directory_path}_{time_stamp}"

		return cls.create_directory(directory_path)

	@classmethod
	def remove_directory(cls, *directory_path: str) -> None:
		"""Removes multiple directories.

		Arguments:
		---------
			*directory_path: /path/to/directory

		Returns:
		-------
			`None`

		"""
		for directory in directory_path:
			if Path(directory).exists():
				try:
					shutil.rmtree(directory)
					logger.debug("Removed directory %s", directory)

				finally:
					logger.error("%s cannot be removed", directory)

			else:
				logger.error("%s does not exits and cannot be removed", directory)

	@classmethod
	def clear_directory(
		cls,
		*directory_path: str,
	) -> None:
		"""Removes all the content of a directory.

		Arguments:
		---------
			*directory_path: /path/to/directory

		Returns:
		-------
			`None`

		"""
		for directory in directory_path:
			files = cls.get_files_in_directory_tree(directory_path=directory)

			for file in files:
				cls.remove_file(file)

			directories = Files.get_content_of_directory(directory_path=directory)

			for item in directories:
				shutil.rmtree(item)

			content = cls.get_content_of_directory(directory_path=directory)

			if content == []:
				logger.debug("Content in %s removed", directory)

			else:
				logger.error(
					"Something went wrong by removing the content in %s",
					directory,
				)
