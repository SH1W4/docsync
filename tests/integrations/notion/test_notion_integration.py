# test_notion_integration.py
from pathlib import Path
from unittest.mock import patch, AsyncMock

import pytest

from docsync.integrations.notion import (
    NotionBridge,
    NotionClient,
    NotionConfig,
    NotionDatabase,
    NotionMapping,
)


@pytest.fixture
def notion_config():
    return NotionConfig(
        token="test_token",
        workspace_id="test_workspace",
        mappings=[NotionMapping(source_path=Path("./docs"), target_id="test_page_id")],
    )


@pytest.fixture
def mock_client():
    with patch("docsync.integrations.notion.bridge.NotionClient", spec=NotionClient) as mock:
        client = mock.return_value
        client.verify_connection = AsyncMock(return_value=True)
        client.get_page = AsyncMock()
        client.get_database = AsyncMock()
        client.create_page = AsyncMock()
        client.update_page = AsyncMock()
        client.get_pages_in_database = AsyncMock(return_value=[])
        yield client


@pytest.fixture
def notion_bridge(notion_config, mock_client):
    return NotionBridge(config=notion_config)


@pytest.mark.asyncio
async def test_notion_bridge_initialization(notion_bridge, mock_client):
    await notion_bridge.initialize()
    assert notion_bridge.client is not None
    assert notion_bridge.config is not None


@pytest.mark.asyncio
async def test_notion_client_connection(mock_client, notion_config):
    # O mock_client já está patcheado para retornar o mock
    # Mas aqui o teste instancia um NOVO NotionClient.
    # Precisamos garantir que este novo também seja mockado ou usar o mock diretamente.
    with patch("docsync.integrations.notion.client.aiohttp.ClientSession") as mock_session:
        client = NotionClient(notion_config)
        # Mockar a resposta de users/me
        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp.headers = {}
        mock_resp.json = AsyncMock(return_value={"id": "user_id"})
        mock_session.return_value.request.return_value.__aenter__.return_value = mock_resp
        
        assert await client.verify_connection() is True


@pytest.mark.asyncio
async def test_notion_page_retrieval(mock_client, notion_config):
    with patch("docsync.integrations.notion.client.aiohttp.ClientSession") as mock_session:
        client = NotionClient(notion_config)
        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp.headers = {}
        mock_resp.json = AsyncMock(return_value={
            "id": "test_id",
            "object": "page",
            "created_time": "2025-06-04T12:00:00Z",
            "last_edited_time": "2025-06-04T12:00:00Z",
            "parent": {"type": "workspace", "workspace": True},
            "properties": {"title": {"title": [{"plain_text": "Test Page"}]}},
        })
        mock_session.return_value.request.return_value.__aenter__.return_value = mock_resp

        page = await client.get_page("test_id")
        assert page.id == "test_id"
        assert page.title == "Test Page"


@pytest.mark.asyncio
async def test_notion_database_retrieval(mock_client, notion_config):
    with patch("docsync.integrations.notion.client.aiohttp.ClientSession") as mock_session:
        client = NotionClient(notion_config)
        
        # Mock para get_database
        mock_db_resp = AsyncMock()
        mock_db_resp.status = 200
        mock_db_resp.headers = {}
        mock_db_resp.json = AsyncMock(return_value={
            "id": "test_db",
            "object": "database",
            "created_time": "2025-06-04T12:00:00Z",
            "last_edited_time": "2025-06-04T12:00:00Z",
            "title": [{"plain_text": "Test Database"}],
            "description": [],
            "properties": {},
        })
        
        # Mock para get_pages_in_database (chamado por _convert_to_notion_database)
        mock_query_resp = AsyncMock()
        mock_query_resp.status = 200
        mock_query_resp.headers = {}
        mock_query_resp.json = AsyncMock(return_value={"results": [], "has_more": False})
        
        # Configurar retornos sequenciais
        mock_session.return_value.request.return_value.__aenter__.side_effect = [mock_db_resp, mock_query_resp]

        db = await client.get_database("test_db")
        assert db.id == "test_db"
        assert db.title == "Test Database"


@pytest.mark.asyncio
async def test_sync_mapping(notion_bridge, tmp_path, mock_client):
    # Criar estrutura de teste
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    test_file = docs_dir / "test.md"
    test_file.write_text("# Test Document")

    # Configurar mapping
    mapping = NotionMapping(source_path=docs_dir, target_id="test_target")
    
    # Mockar get_page para o _setup_mapping que é chamado no sync
    mock_client.get_page.return_value = {"id": "test_target", "title": "Test Target"}

    # Testar sincronização
    await notion_bridge._sync_mapping(mapping)
    # Aqui adicionaremos mais verificações quando implementarmos
    # a lógica completa de sincronização
