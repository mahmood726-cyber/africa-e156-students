"""Import-smoke + pure-function tests for the Africa E156 build script."""
import importlib.util
import os
import sys

import pytest

_SCRIPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "build.py")


def _load():
    sys.path.insert(0, os.path.dirname(_SCRIPT))
    spec = importlib.util.spec_from_file_location("e156_build", _SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_module_imports():
    assert _load() is not None


def test_split_sentences_caps_at_seven():
    mod = _load()
    body = " ".join(f"Sentence number {i} here." for i in range(1, 11))
    out = mod.split_sentences(body)
    assert len(out) == 7  # E156 contract: at most 7 sentences


def test_split_sentences_short_body_preserved():
    mod = _load()
    out = mod.split_sentences("First one. Second one. Third one.")
    assert len(out) == 3
    assert out[0].startswith("First")


def test_split_sentences_empty():
    mod = _load()
    assert mod.split_sentences("") == [""]


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
