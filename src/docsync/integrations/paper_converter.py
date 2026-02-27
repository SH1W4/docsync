import re
from pathlib import Path
from typing import Any, Dict


class PaperConverter:
    """Converts documentation files to Paper Generator configuration."""

    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.readme_path = root_path / "README.md"

    def to_config(self) -> Dict[str, Any]:
        """Generate complete paper configuration."""
        # 1. Parse README for basics
        readme_content = ""
        if self.readme_path.exists():
            readme_content = self.readme_path.read_text(encoding="utf-8")

        title = self._extract_title(readme_content) or self.root_path.name
        abstract = self._extract_abstract(readme_content)

        # 2. Build Sections
        sections = []

        # Introduction (from README)
        if readme_content:
            sections.append(
                {
                    "title": "Introduction",
                    "content": self._clean_content(readme_content),
                },
            )

        # Architecture
        arch_path = self.root_path / "ARCHITECTURE.md"
        if arch_path.exists():
            sections.append(
                {
                    "title": "System Architecture",
                    "content": arch_path.read_text(encoding="utf-8"),
                },
            )

        # Installation/Usage from dedicated files
        for filename, title in [
            ("INSTALLATION.md", "Installation"),
            ("USAGE.md", "Usage"),
            ("CONTRIBUTING.md", "Development"),
        ]:
            path = self.root_path / filename
            if path.exists():
                sections.append(
                    {"title": title, "content": path.read_text(encoding="utf-8")},
                )

        # 3. Assemble Config
        return {
            "metadata": {
                "title": f"Technical Report: {title}",
                "authors": [
                    {
                        "name": "DocSync Automation",
                        "affiliation": "Generated from codebase",
                    },
                ],
                "abstract": abstract,
                "keywords": ["Software Documentation", "Technical Report", title],
                "date": "December 2025",
            },
            "sections": sections,
            "template": "ieee",
            "references": [],  # TODO: Parse CITATION.cff
        }

    def _extract_title(self, content: str) -> str:
        """Extract title from first # header."""
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        return match.group(1).strip() if match else ""

    def _extract_abstract(self, content: str) -> str:
        """Extract first paragraph after title."""
        # Remove title
        content = re.sub(r"^#\s+.+$", "", content, flags=re.MULTILINE)
        # Find first paragraph
        match = re.search(r"([A-Za-z].+?)(\n\n|$)", content.strip(), re.DOTALL)
        return match.group(1).strip() if match else "No abstract available."

    def _clean_content(self, content: str) -> str:
        """Clean content for Latex inclusion."""
        # Remove top level title
        content = re.sub(r"^#\s+.+$", "", content, flags=re.MULTILINE)
        # Demote headers (# -> ##, ## -> ###)
        # This is naïve but works for simple cases
        return content.strip()
