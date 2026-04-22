import os
import pytest

# pytest.ini adds both `src` and `src/lib` to pythonpath.
# Production modules (bbdd.py, libstats.py, ods.py ...) use bare imports:
#   from bbdd import Bbdd
# To ensure monkeypatching the class affects ALL callers we must import via
# the SAME bare name here in the fixtures.

from bbdd import Bbdd  # noqa: E402


@pytest.fixture
def db_memory(tmp_path, monkeypatch):
    """Isolated SQLite database initialised from database.sql.

    Monkeypatches Bbdd's class-level directory and name so that every Bbdd()
    instance created during the test -- including those inside LibStats, Ods,
    etc. -- connects to the same temporary file.  The file is removed
    automatically by pytest's tmp_path fixture after the test.
    """
    monkeypatch.setattr(Bbdd, "directory", str(tmp_path) + os.sep)
    monkeypatch.setattr(Bbdd, "name", "test.sqlite3")
    bd = Bbdd()
    yield bd
    bd.close()
