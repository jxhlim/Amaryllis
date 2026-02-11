from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


@dataclass
class DownloadResult:
    downloaded_files: list[Path]
    output_folder: Path


@dataclass
class DraftResult:
    draft_path: Path
    payload: dict


class PinterestDownloadError(RuntimeError):
    pass


class PinterestDownloader:
    """Uses gallery-dl to fetch board images in highest available quality."""

    def __init__(self, gallery_dl_cmd: str = "gallery-dl") -> None:
        self.gallery_dl_cmd = gallery_dl_cmd

    def download_board(self, board_url: str, workspace: Path, limit: int | None = None) -> DownloadResult:
        workspace.mkdir(parents=True, exist_ok=True)

        cmd = [
            self.gallery_dl_cmd,
            "--write-metadata",
            "--dest",
            str(workspace),
            board_url,
        ]
        if limit:
            cmd.extend(["--range", f"1-{limit}"])

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except FileNotFoundError as exc:
            raise PinterestDownloadError(
                "gallery-dl is not installed. Install it with `pip install gallery-dl`."
            ) from exc
        except subprocess.CalledProcessError as exc:
            message = exc.stderr.strip() or exc.stdout.strip() or "Unknown downloader failure"
            raise PinterestDownloadError(f"gallery-dl failed: {message}") from exc

        files = sorted(path for path in workspace.rglob("*") if path.suffix.lower() in IMAGE_EXTENSIONS)
        if not files:
            raise PinterestDownloadError(
                "No images were downloaded. Verify board URL, credentials, and access rights."
            )
        return DownloadResult(downloaded_files=files, output_folder=workspace)


class DayOrganizer:
    """Organizes images under YYYY-MM-DD folders."""

    def organize(self, files: Iterable[Path], destination_root: Path) -> list[Path]:
        destination_root.mkdir(parents=True, exist_ok=True)
        moved_files: list[Path] = []

        for source in files:
            created_at = self._guess_file_date(source)
            day_folder = destination_root / created_at.strftime("%Y-%m-%d")
            day_folder.mkdir(parents=True, exist_ok=True)

            target = day_folder / source.name
            if target.exists():
                target = day_folder / f"{target.stem}_{int(datetime.now().timestamp())}{target.suffix}"

            shutil.move(str(source), target)
            moved_files.append(target)

        return moved_files

    def _guess_file_date(self, image_path: Path) -> datetime:
        metadata_path = image_path.with_suffix(".json")
        if metadata_path.exists():
            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                for field in ("date", "created_at", "created"):
                    if field in metadata and metadata[field]:
                        return datetime.fromisoformat(str(metadata[field]).replace("Z", "+00:00"))
            except (json.JSONDecodeError, ValueError, TypeError):
                pass
        return datetime.fromtimestamp(image_path.stat().st_mtime)


class InstagramDraftBuilder:
    """Builds lightweight carousel drafts as JSON for manual review/posting."""

    def build_draft(self, board_url: str, images: list[Path], drafts_folder: Path) -> DraftResult:
        drafts_folder.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        draft_path = drafts_folder / f"instagram_draft_{timestamp}.json"

        tags = self._infer_tags(board_url)
        caption = (
            "Fresh inspiration drop ✨\n"
            + "Save your favorites from this carousel and follow for more.\n\n"
            + " ".join(f"#{tag}" for tag in tags)
        )

        payload = {
            "created_at": datetime.now().isoformat(),
            "source": board_url,
            "type": "carousel",
            "image_paths": [str(path) for path in images],
            "caption": caption,
            "status": "draft",
            "notes": "Review image order/caption before publishing in Instagram app.",
        }
        draft_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return DraftResult(draft_path=draft_path, payload=payload)

    def _infer_tags(self, board_url: str) -> list[str]:
        chunks = [piece for piece in board_url.lower().replace("-", " ").split("/") if piece]
        words: list[str] = []
        for chunk in chunks:
            for word in chunk.split():
                clean = "".join(ch for ch in word if ch.isalnum())
                if clean and clean not in {"https", "http", "www", "com", "pinterest"}:
                    words.append(clean)
        seed = words[-5:] if words else ["inspiration", "carousel", "design"]
        return [*dict.fromkeys(seed), "instagram", "moodboard"]


class Workflow:
    def __init__(
        self,
        downloader: PinterestDownloader | None = None,
        organizer: DayOrganizer | None = None,
        drafts: InstagramDraftBuilder | None = None,
    ) -> None:
        self.downloader = downloader or PinterestDownloader()
        self.organizer = organizer or DayOrganizer()
        self.drafts = drafts or InstagramDraftBuilder()

    def run(
        self,
        board_url: str,
        output_root: Path,
        max_images: int | None,
    ) -> tuple[list[Path], DraftResult]:
        staging = output_root / "_staging"
        result = self.downloader.download_board(board_url=board_url, workspace=staging, limit=max_images)
        organized = self.organizer.organize(result.downloaded_files, output_root / "images_by_day")
        draft = self.drafts.build_draft(board_url, organized, output_root / "drafts")
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        return organized, draft
