"""Tests for the file integrity monitor (FIM) hashing and baseline logic."""

import sys
import os
import json
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "file-integrity"))

from fim import calculate_file_hash, build_baseline


class TestFileHashCalculation:
    """Unit tests for hash calculation."""

    def test_sha256_hash_deterministic(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("hello world")
            tmp_path = f.name
        try:
            hash1 = calculate_file_hash(tmp_path, "sha256")
            hash2 = calculate_file_hash(tmp_path, "sha256")
            assert hash1 is not None
            assert hash1 == hash2
        finally:
            os.unlink(tmp_path)

    def test_different_content_different_hash(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f1:
            f1.write("file one content")
            path1 = f1.name
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f2:
            f2.write("file two content")
            path2 = f2.name
        try:
            assert calculate_file_hash(path1) != calculate_file_hash(path2)
        finally:
            os.unlink(path1)
            os.unlink(path2)

    def test_md5_algorithm(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("test md5")
            tmp_path = f.name
        try:
            h = calculate_file_hash(tmp_path, "md5")
            assert h is not None
            assert len(h) == 32  # MD5 produces 32 hex chars
        finally:
            os.unlink(tmp_path)

    def test_nonexistent_file_returns_none(self):
        result = calculate_file_hash("/nonexistent/file.txt")
        assert result is None


class TestBuildBaseline:
    """Tests for baseline building."""

    def test_baseline_captures_all_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            for i in range(3):
                with open(os.path.join(tmpdir, f"file{i}.txt"), "w") as f:
                    f.write(f"content {i}")

            output_path = os.path.join(tmpdir, "baseline.json")
            build_baseline(tmpdir, output_path)

            with open(output_path) as f:
                baseline = json.load(f)

            # 3 data files + baseline.json itself = 4 entries
            assert len(baseline) >= 3
