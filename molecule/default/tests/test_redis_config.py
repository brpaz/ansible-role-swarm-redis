import testinfra
import pytest

CONFIG_FILE = "/etc/redis/redis.conf"
REDIS_PORT = 6379


def test_redis_conf_exists(host):
    """Test that Redis configuration file exists with proper permissions."""
    f = host.file(CONFIG_FILE)
    assert f.exists, f"Redis config file {CONFIG_FILE} does not exist"
    assert f.is_file, f"Redis config {CONFIG_FILE} is not a file"
    assert f.user == "root", f"Redis config not owned by root"
    assert f.group == "root", f"Redis config group not root"
    assert oct(f.mode) == "0o640", f"Redis config has incorrect permissions"


@pytest.mark.parametrize(
    "setting,expected",
    [
        ("bind", "0.0.0.0"),
        ("port", str(REDIS_PORT)),
    ],
)
def test_redis_conf_settings(host, setting, expected):
    """Test that Redis configuration contains expected settings."""
    f = host.file(CONFIG_FILE)
    contents = f.content_string
    assert (
        f"{setting} {expected}" in contents
    ), f"Setting '{setting}' with value '{expected}' not found"
