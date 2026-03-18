from automation_functions.functions import *
import pytest

def test_open_chrome(mocker):
    mocker.patch('webbrowser.open')
    assert open_chrome() is None
    webbrowser.open.assert_called_with("https://www.google.com")

def test_get_cpu_usage():
    usage = get_cpu_usage()
    assert isinstance(usage, float)
    assert 0 <= usage <= 100

def test_run_shell_command():
    result = run_shell_command("echo hello")
    assert result["returncode"] == 0
    assert "hello" in result["stdout"]