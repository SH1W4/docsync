# test_notion_types.py
from datetime import datetime

from docsync.integrations.notion.types import NotionDatabase, NotionPage


def test_notion_page_creation():
    page = NotionPage(
        id="test_id",
        title="Test Page",
        properties={"key": "value"},
    )

    assert page.id == "test_id"
    assert page.title == "Test Page"
    assert isinstance(page.last_edited_time, datetime)
    assert page.properties == {"key": "value"}


def test_notion_database_creation():
    db = NotionDatabase(
        id="test_db",
        title="Test Database",
        description="Test Description",
        properties={"field": {"type": "text"}},
        pages=[],
    )

    assert db.id == "test_db"
    assert db.title == "Test Database"
    assert db.description == "Test Description"
    assert db.properties == {"field": {"type": "text"}}
    assert isinstance(db.pages, list)
    assert isinstance(db.last_edited_time, datetime)
