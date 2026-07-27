from pathlib import Path
import runpy


def test_main_prints_hello_world(capsys):
    runpy.run_path(Path(__file__).parents[1] / "src" / "main.py")

    assert capsys.readouterr().out == "Hello, world!\n"
