"""Test cases for the main.py file"""

import builtins
import json

import main


def test_main():
    """Tests the root endpoint"""
    assert main.main() == {"hello": "world"}


def test_convert():
    """Tests the conversion endpoint"""
    assert main.convert("PA", "Pittsburgh") == {
        "lat": "40.4416941",
        "long": "-79.9900861",
    }


# ----------- Written for Day 1 - Afternoon ----------- #


def test_get_comments(tmp_path, monkeypatch):
    original_open = open
    monkeypatch.setattr(main.os, "listdir", lambda: [])  # type: ignore
    assert main.get_comments() == []

    temp_comments = tmp_path / "comments.json"
    cmt = [main.Comment(comment="testing", created=None)]
    temp_comments.write_text(json.dumps([c.model_dump() for c in cmt]))

    def mock_open(path, mode, encoding="utf-8"):
        if str(path) == str(temp_comments) or path == "comments.json":
            return original_open(temp_comments, mode, encoding=encoding)
        return original_open(path, mode, encoding=encoding)

    monkeypatch.setattr(builtins, "open", mock_open)
    monkeypatch.setattr(main.os, "listdir", lambda: ["comments.json"])  # type: ignore
    comments = main.get_comments()
    assert len(comments) == 1


def test_post_comment(tmp_path, monkeypatch):
    original_open = open
    temp_comments = tmp_path / "comments.json"

    initial_comments = [{"comment": "existing", "created": None}]
    temp_comments.write_text(json.dumps(initial_comments))

    def mock_open(path, mode="r", encoding="utf-8"):
        if str(path) == str(temp_comments) or path == "comments.json":
            return original_open(temp_comments, mode, encoding=encoding)
        return original_open(path, mode, encoding=encoding)

    monkeypatch.setattr(builtins, "open", mock_open)
    monkeypatch.setattr(main.os, "listdir", lambda: ["comments.json"])

    # Create a mock datetime class with .now() method
    class MockDateTime:  # pylint: disable=too-few-public-methods
        @staticmethod
        def now(tz):  # pylint: disable=unused-argument
            return "fixed_timestamp"

    monkeypatch.setattr("main.datetime", MockDateTime)

    new_comment = main.Comment(comment="new one", created=None)
    main.post_comment(new_comment)

    with temp_comments.open("r") as f:
        result = json.load(f)

    assert len(result) == 2
    assert result[-1]["comment"] == "new one"
    assert result[-1]["created"] == "fixed_timestamp"
