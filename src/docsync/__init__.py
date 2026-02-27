"""DocSync - Documentation synchronization and ESG report generation.

This package provides tools for:
- ESG report generation using templates
- Document synchronization across projects
- File watching and automatic updates
- Notion integration for documentation workflows
"""

__version__ = "0.1.0"
__author__ = "GUARDRIVE Team"
__email__ = "team@guardrive.io"

from .core import (
    DocSync,
)
from .exceptions import (
    DocSyncError,
    ReportGenerationError,
    TemplateError,
)
from .sync_manager import SyncManager

__all__ = [
    "DocSync",
    "DocSyncError",
    "ReportGenerationError",
    "SyncManager",
    "TemplateError",
]
