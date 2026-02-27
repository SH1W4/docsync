import asyncio
import logging
from pathlib import Path

from git import Repo

logger = logging.getLogger("aiogit-sovereign")


class Repository:
    """Sovereign Adapter for GitPython to match aiogit interface."""

    def __init__(self, repo_path: Path):
        self.path = Path(repo_path)
        self._repo = None

    @classmethod
    async def create(cls, path: Path):
        """Mock create - returns instance to be initialized."""
        return cls(path)

    @classmethod
    async def open(cls, path: Path):
        """Opens an existing repository."""
        instance = cls(path)
        try:
            instance._repo = Repo(path)
            return instance
        except Exception as e:
            logger.error(f"Failed to open repo at {path}: {e}")
            raise

    async def init(self):
        """Initializes a new git repository."""
        loop = asyncio.get_event_loop()
        self._repo = await loop.run_in_executor(None, Repo.init, self.path)

    async def add_all(self):
        """Adds all changes to the index."""
        if not self._repo:
            self._repo = Repo(self.path)

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._repo.git.add, "--all")

    async def commit(self, message: str):
        """Commits changes with the given message."""
        if not self._repo:
            self._repo = Repo(self.path)

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._repo.index.commit, message)
