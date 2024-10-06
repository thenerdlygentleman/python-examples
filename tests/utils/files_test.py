import datetime
from pathlib import Path

from src.system.files import Files


def test_get_content_of_directory_is_list(tmp_path: Path) -> None:
	"""Check if function is returning a list."""
	Files.create_file(
		f"{tmp_path}/file_1.txt",
		f"{tmp_path}/file_2.py",
		f"{tmp_path}/file_3",
	)
	content_test = Files.get_content_of_directory(directory_path=tmp_path)
	assert isinstance(content_test, list)


def test_get_content_of_directory(tmp_path: Path) -> None:
	"""Check if content of directory is returned correctly."""
	Files.create_file(
		f"{tmp_path}/file_1.txt",
		f"{tmp_path}/file_2.py",
		f"{tmp_path}/file_3",
	)
	content_real = Path(tmp_path).glob("*")
	content_real_list = []
	for item in content_real:
		content_real_list.append(item)
	content_real_list.sort()
	content_test = Files.get_content_of_directory(directory_path=tmp_path)
	assert content_real_list == content_test


def test_get_content_of_directory_with_search_name(tmp_path: Path) -> None:
	"""Check if content of directory with a search name is returned correctly."""
	search_name = "file"
	Files.create_file(
		f"{tmp_path}/file",
		f"{tmp_path}/textfile.txt",
		f"{tmp_path}/script.sh",
	)
	content_real = Path(tmp_path).glob(f"*{search_name}*")
	content_real_list = []
	for item in content_real:
		content_real_list.append(item)
	content_real_list.sort()
	content_test = Files.get_content_of_directory(
		directory_path=tmp_path,
		search_name=search_name,
	)
	assert content_real_list == content_test


def test_get_files_in_directory_tree_is_list(tmp_path: Path) -> None:
	"""Checks if function is returning a list."""
	Files.create_directory(
		f"{tmp_path}/directory_1",
		f"{tmp_path}/directory_2",
		f"{tmp_path}/directory_3",
	)
	for i in range(1, 3):
		Files.create_file(
			f"{tmp_path}/directory_{i}/file_1",
			f"{tmp_path}/directory_{i}/file_2",
			f"{tmp_path}/directory_{i}/file_3",
		)
	directory_content = Files.get_files_in_directory_tree(directory_path=tmp_path)
	assert isinstance(directory_content, list)


def test_get_files_in_directory_tree(tmp_path: Path) -> None:
	"""Check if all files in a directory tree are returned."""
	file_list = []
	Files.create_directory(
		f"{tmp_path}/directory_1",
		f"{tmp_path}/directory_2",
		f"{tmp_path}/directory_3",
	)
	for i in range(1, 3):
		files = Files.create_file(
			f"{tmp_path}/directory_{i}/file_1",
			f"{tmp_path}/directory_{i}/file_2",
			f"{tmp_path}/directory_{i}/file_3",
		)
		file_list.extend(files)
	directory_content = Files.get_files_in_directory_tree(directory_path=tmp_path)
	file_list.sort()
	assert file_list == directory_content


def test_create_file(tmp_path: Path) -> None:
	"""Test if a files is created."""
	file_path_1 = f"{tmp_path}/file_1.txt"
	file_path_2 = f"{tmp_path}/file_2.txt"
	Files.create_file(file_path_1, file_path_2)
	assert Path(file_path_1).is_file()
	assert Path(file_path_2).is_file()


def test_copy_file_pass(tmp_path: Path) -> None:
	"""Test if the files was copied."""
	directory_1 = f"{tmp_path}/directory_1"
	directory_2 = f"{tmp_path}/directory_2"
	file_1 = f"{directory_1}/file_1"
	file_2 = f"{directory_1}/file_2"
	Files.create_directory(directory_1, directory_2)
	Files.create_file(file_1, file_2)
	Files.copy_file(file_1, file_2, destination=directory_2)
	assert Path(f"{directory_2}/{Path(file_1).name}").is_file()
	assert Path(f"{directory_2}/{Path(file_2).name}").is_file()


def test_copy_file_fail_file_not_exits(tmp_path: Path) -> None:
	"""Test if a file is not copied, because it does not exits."""
	Files.copy_file(f"{tmp_path}/fake_file", destination=tmp_path)
	assert not Path(f"{tmp_path}/fake_file").is_file()


def test_copy_file_pass_file_already_exits(tmp_path: Path) -> None:
	"""Test if copy file fails, because the file already exits."""
	directory_1 = f"{tmp_path}/directory_1"
	directory_2 = f"{tmp_path}/directory_2"
	file_1 = f"{directory_1}/file_1"
	file_2 = f"{directory_1}/file_2"
	file_1_copy = f"{directory_2}/file_1"
	Files.create_directory(directory_1, directory_2)
	Files.create_file(file_1, file_2, file_1_copy)
	copy_item = Files.copy_file(file_1, file_2, destination=directory_2)
	assert Path(f"{directory_2}/{Path(file_2).name}").is_file()
	assert copy_item == Path(f"{directory_2}/{Path(file_2).name}")


def test_rename_file_with_suffix(tmp_path: Path) -> None:
	"""Test if rename a file without syntax is possible."""
	file_1 = f"{tmp_path}/file_1.txt"
	new_name = "this_is_a_new_name"
	Files.create_file(file_1)
	Files.rename_file(file_path=file_1, new_name=new_name, autorun=True)
	new_file = f"{tmp_path}/{new_name}{Path(file_1).suffix}"
	assert Path(new_file).is_file()


def test_rename_file_without_suffix(tmp_path: Path) -> None:
	"""Test if rename a file with suffix is possible."""
	file_1 = f"{tmp_path}/file_1"
	new_name = "this_is_a_new_name"
	Files.create_file(file_1)
	Files.rename_file(file_path=file_1, new_name=new_name, autorun=True)
	new_file = f"{tmp_path}/{new_name}{Path(file_1).suffix}"
	assert Path(new_file).is_file()


def test_rename_multiple_files_with_same_name(tmp_path: Path) -> None:
	"""Test if renaming multiple files with the same name is possible."""
	new_name = "new_name"
	Files.create_file(f"{tmp_path}/{new_name}.txt")
	for i in range(1, 3):
		file = f"{tmp_path}/file.txt"
		Files.create_file(file)
		assert Path(file).is_file()
		Files.rename_file(file_path=file, new_name=new_name, autorun=True)
		new_path = f"{tmp_path}/{new_name}_{i}{Path(file).suffix}"
		assert Path(new_path).is_file()


def test_create_directory(tmp_path: Path) -> None:
	"""Test if creating a directory is possible."""
	directory_path = f"{tmp_path}/directory_1"
	Files.create_directory(directory_path)
	assert Path(directory_path).is_dir()


def test_create_time_directory(tmp_path: Path) -> None:
	"""Test if creating a time directory is possible."""
	time = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
	directory_name = "directory"
	directory_path = f"{tmp_path}/{directory_name}_{time}"
	Files.create_time_directory(directory_path=f"{tmp_path}/{directory_name}")
	assert Path(directory_path).is_dir()


def test_remove_directory(tmp_path: Path) -> None:
	"""Test if removing a directory is possible."""
	directory = f"{tmp_path}/directory"
	Files.create_directory(directory)
	assert Path(directory).is_dir()
	Files.remove_directory(directory)
	assert not Path(directory).exists()


def test_remove_file_pass(tmp_path: Path) -> None:
	"""Test if removinf a file is possible."""
	file = f"{tmp_path}/file"
	Files.create_file(file)
	Files.remove_file(file)
	assert not Path(file).is_file()


def test_remove_file_fail(tmp_path: Path) -> None:
	"""Test if removing a directory is not possible."""
	directory = f"{tmp_path}/directory"
	Files.create_directory(directory)
	Files.remove_file(directory)
	assert Path(directory).is_dir()


def test_clear_directory(tmp_path: Path) -> None:
	"""Test if clearing a directory is possible."""
	directory_1 = f"{tmp_path}/directory_1"
	directory_2 = f"{tmp_path}/directory_2"
	directory_3 = f"{directory_1}/directory_3"
	file_1 = f"{directory_1}/file_1"
	file_2 = f"{directory_1}/file_2"
	file_3 = f"{directory_2}/file_3"
	Files.create_directory(directory_1, directory_2, directory_3)
	Files.create_file(file_1, file_2, file_3)
	Files.clear_directory(directory_1)
	assert Path(directory_1).exists()
	content_1 = Files.get_content_of_directory(directory_path=directory_1)
	assert content_1 == []
	content_2 = Files.get_content_of_directory(directory_path=directory_2)
	assert content_2 != []
	content_tmp = Files.get_content_of_directory(directory_path=tmp_path)
	assert content_tmp != []
	file_4 = Files.create_file(f"{tmp_path}/directory_1/file_4")
	assert file_4.is_file()
