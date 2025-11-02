from .base_repo import BaseRepository
from .podcast_repo import PodcastRepository
from .source_repo import SourceRepository

# --- Singleton Instances ---
podcast_repo = PodcastRepository()
source_repo = SourceRepository()

__all__ = [
    "BaseRepository",
    "PodcastRepository",
    "SourceRepository",
    "podcast_repo",
    "source_repo",
]