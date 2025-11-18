import subprocess
import sys

def test_cli_help():
    result = subprocess.run(
        [sys.executable, "-m", "raffle_tickets.cli", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Generar papeletas" in result.stdout


def test_cli_digits_validation():
    result = subprocess.run(
        [sys.executable, "-m", "raffle_tickets.cli", "-d", "7"],
        capture_output=True,
        text=True
    )
    assert result.returncode != 0
    assert "debe ser un numero entre 1 y 4" in result.stderr.lower()
