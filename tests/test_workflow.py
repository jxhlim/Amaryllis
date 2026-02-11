from __future__ import annotations

import json
from pathlib import Path

from src.validation import looks_like_pinterest_board
from src.workflow import DayOrganizer, InstagramDraftBuilder


def test_day_organizer_uses_metadata_date(tmp_path: Path):
    source = tmp_path / "staging"
    source.mkdir()
    image = source / "photo.jpg"
    image.write_bytes(b"x")
    metadata = source / "photo.json"
    metadata.write_text(json.dumps({"date": "2026-01-04T10:00:00Z"}), encoding="utf-8")

    organizer = DayOrganizer()
    moved = organizer.organize([image], tmp_path / "out")

    assert len(moved) == 1
    assert "2026-01-04" in str(moved[0])
    assert moved[0].exists()


def test_instagram_draft_builder_creates_json(tmp_path: Path):
    image = tmp_path / "img.jpg"
    image.write_bytes(b"x")

    builder = InstagramDraftBuilder()
    draft = builder.build_draft(
        "https://www.pinterest.com/user/minimal-home-ideas/",
        [image],
        tmp_path / "drafts",
    )

    payload = json.loads(draft.draft_path.read_text(encoding="utf-8"))
    assert payload["type"] == "carousel"
    assert payload["status"] == "draft"
    assert payload["image_paths"] == [str(image)]
    assert "#instagram" in payload["caption"]


def test_pinterest_board_url_validation():
    assert looks_like_pinterest_board("https://www.pinterest.com/someuser/home-decor/")
    assert not looks_like_pinterest_board("https://example.com/not-pinterest")
    assert not looks_like_pinterest_board("https://www.pinterest.com/justonepart")
