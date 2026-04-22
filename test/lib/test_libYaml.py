import os
import pytest
from libyaml import LibYaml


@pytest.fixture
def yaml_file(tmp_path):
    path = str(tmp_path / "test.yml")
    yield path
    if os.path.exists(path):
        os.remove(path)


def test_load_returns_default_config(yaml_file):
    lib = LibYaml(yaml_file)
    config = lib.load()
    assert "stake" in config
    assert config["stake"]["percentage"] == 1.0


def test_save_and_reload(yaml_file):
    lib = LibYaml(yaml_file)
    lib.config = {"test": "valor"}
    lib.save()
    reloaded = lib.load()
    assert reloaded == {"test": "valor"}
