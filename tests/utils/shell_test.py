from tests.conftest import only_as_root, only_as_user, only_on_linux
from src.system.shell import Shell


@only_on_linux
def test_execute_command_type_stdout() -> None:
	"""Perform a shell command to stdout."""
	output = Shell().execute_command(command="whoami")
	assert isinstance(output, tuple)
	assert isinstance(output[0], list)
	assert isinstance(output[0][0], str)


@only_on_linux
def test_execute_command_type_stderr() -> None:
	"""Perform a shell command to stderr."""
	output = Shell().execute_command(command="cat this_is_not_a_file")
	assert isinstance(output, tuple)
	assert isinstance(output[1], list)
	assert isinstance(output[1][0], str)


@only_on_linux
@only_as_root
def test_execute_command_root() -> None:
	"""Perform a shell command with root user."""
	root = Shell(root=True).execute_command(command="whoami")
	assert root[0][0] == "root"


@only_on_linux
@only_as_user
def test_execute_command_user() -> None:
	"""Perform a shell command with user."""
	user = Shell(root=False).execute_command(command="whoami")
	assert user[0][0] == "edward"
