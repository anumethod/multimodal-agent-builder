import subprocess
import hashlib
import os
import pytest

DATA_KINDS = ["testing", "training", "validation"]

# Directory where you should place small fixture chunks for testing
FIXTURE_BASE = "train-test-validate/chunks/fixtures"
REASSEMBLY_SCRIPT = "scripts/reassemble_files.sh"

@pytest.mark.parametrize("kind", DATA_KINDS)
def test_reassembly_kind(tmp_path, kind):
    """
    Runs the reassembly for each dataset kind using fixture data, verifies that at least one file is produced,
    and (optionally) checks its checksum if you provide KNOWN_GOOD_CHECKSUMS below.
    """
    fixtures_dir = os.path.join(FIXTURE_BASE, f"ML-{kind.capitalize()}")
    if not os.path.isdir(fixtures_dir):
        pytest.skip(f"No fixture data for kind {kind} (directory {fixtures_dir} missing)")

    # Call the reassembly script (dry run so nothing is overwritten)
    result = subprocess.run([
        "bash", REASSEMBLY_SCRIPT,
        "--kind", kind,
        "--verbose"
    ], capture_output=True, text=True)
    assert result.returncode == 0, f"Reassembly failed ({kind}): {result.stderr or result.stdout}"
    # Optionally validate produced output/checksum here

# Optionally, extend with BAD_HOSTILE_FIXTUREs or corruption tests if you want
# to simulate errors/missing chunks for negative coverage.

# KNOWN_GOOD_CHECKSUMS = {...} # If you have known good outputs, you can hash and check here.

# You can run these tests via:
#   pytest tests/reassembly/test_matrix.py

