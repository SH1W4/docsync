# DocSync 🚀

<div align="center">

![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-beta-orange.svg)
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

**Advanced technical documentation synchronization and management system**

*Bidirectional sync between local files and Notion with AI-enhanced processing*

[🇧🇷 Português](./docs/pt-br/README.md) | 🇺🇸 English

</div>

## ✨ Key Features

🔄 **Bidirectional Sync**: Keep local files and Notion always in sync  
🤖 **AI Multi-Provider**: Support for OpenAI, Claude, and Gemini  
🔌 **MCP Server**: Model Context Protocol for external agent integration  
📊 **ESG Templates**: Flexible system for professional reports and documentation  
⚡ **Real-time**: Live monitoring and synchronization  
🛡️ **Auto Backup**: Robust versioning and backup system  
🎨 **Rich CLI**: Intuitive interface with Rich for better UX  

## 📊 Market Potential

- **TAM**: $45+ billion (technical documentation market)
- **MVP Timeline**: 4-6 months development  
- **Projected ROI**: 450-1,200% over 5 years

📋 [View complete market analysis](./ANALISE_MERCADO_VIABILIDADE.md)

## 🚀 Quick Installation

```bash
# Via pip (recommended)
pip install docsync

# Or local development
git clone https://github.com/NEO-SH1W4/docsync.git
cd docsync
pip install -e ".[dev]"
```

## 💡 Quick Start

### 1. Basic Setup
```python
from docsync import DocSync

# Initialize project
sync = DocSync()
sync.configure()
```

### 2. AI-Powered Documentation Improvement
```bash
# Improve documentation with AI (OpenAI by default)
docsync improve README.md

# Use Claude
docsync improve README.md --provider claude

# Use Gemini with specific model
docsync improve README.md --provider gemini --model gemini-2.0-flash-exp
```

**Environment Variables:**
```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic Claude
export ANTHROPIC_API_KEY="sk-ant-..."

# Google Gemini
export GOOGLE_API_KEY="AI..."
```

### 3. MCP Server for External Agents
```bash
# Start MCP server (for Claude Desktop, IDEs, etc.)
docsync serve

# Connect from Claude Desktop - add to claude_desktop_config.json:
{
  "mcpServers": {
    "docsync": {
      "command": "docsync",
      "args": ["serve"]
    }
  }
}
```

### 4. Notion Integration (Coming Soon)
```python
from docsync.integrations.notion import NotionBridge, NotionConfig

config = NotionConfig(
    token='your_notion_token',
    workspace_id='your_workspace'
)

bridge = NotionBridge(config)
await bridge.sync()
```

### 3. Interactive CLI
```bash
# Sync directory
docsync sync ./docs --config config.yaml

# Generate ESG report
docsync generate --template esg-report --output ./reports
```

## 🧩 Supported Integrations

| Platform | Status | Description |
|----------|--------|-------------|
| 🤖 **OpenAI** | ✅ Complete | GPT-4o-mini, GPT-4o for documentation analysis |
| 🤖 **Claude** | ✅ Complete | Claude 3.5 Haiku/Sonnet for AI improvements |
| 🤖 **Gemini** | ✅ Complete | Google Gemini 2.0 Flash for content generation |
| 🔌 **MCP** | ✅ Complete | Model Context Protocol server for agents |
| 🎯 **Notion** | 🚧 Beta | Bidirectional sync with pages and databases |
| 📝 **Markdown** | ✅ Complete | Advanced markdown file processing |
| 🔗 **Git** | ✅ Complete | Repository integration for versioning |
| 🌐 **APIs** | 🚧 Beta | Automatic REST API documentation |

## 📚 Documentation

- 🏃‍♂️ [**Quick Start Guide**](./QUICKSTART.md)
- 🎯 [**Notion Integration**](./examples/notion/GUIDE.md)
- 🤝 [**Contributing Guide**](./CONTRIBUTING.md)
- 📋 [**Changelog**](./CHANGELOG.md)
- 💼 [**Business Analysis**](./ANALISE_MERCADO_VIABILIDADE.md)

## 🛠️ For Developers

### Code Quality
```bash
# Formatting and linting
black . && isort . && flake8

# Tests with coverage
pytest --cov=docsync --cov-report=html

# Type checking
mypy src/
```

### Project Structure
```
docsync/
├── src/docsync/          # Main code
│   ├── core/             # Sync engine
│   ├── integrations/     # Integrations (Notion, etc.)
│   ├── templates/        # Template system
│   └── utils/            # Utilities and filters
├── templates/            # Document templates
├── examples/             # Practical examples
└── tests/                # Unit tests
```

## 🤝 Contributing

Contributions are very welcome! This project has the potential to positively impact the developer community.

1. 🍴 Fork the project
2. 🌟 Create your feature branch
3. ✅ Add tests
4. 📝 Update documentation
5. 🚀 Open a Pull Request

See the [complete contribution guide](./CONTRIBUTING.md).

## 🎯 Roadmap

### ✅ v0.2.0 (Released - November 2025)
- ✅ Multi-LLM provider support (OpenAI, Claude, Gemini)
- ✅ MCP server for external agents
- ✅ AI-powered documentation improvement

### v0.3.0 (Q1 2025)
- 🔗 GitHub/GitLab integration
- 🧠 Local LLM support (Ollama)
- 🧩 Plugin system

### v0.4.0 (Q2 2025)
- 🌐 Web interface
- 📊 Analytics dashboard
- 👥 Multi-tenant support

### v1.0.0 (Q3 2025)
- 🏢 Enterprise features
- 📞 Professional support
- 🚀 Production release

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

Built with ❤️ for the developer community. If this project helped you, consider giving it a ⭐!

---

<div align="center">

**[🏠 Homepage](https://github.com/NEO-SH1W4/docsync) • [📖 Docs](https://github.com/NEO-SH1W4/docsync#readme) • [🐛 Issues](https://github.com/NEO-SH1W4/docsync/issues) • [💬 Discussions](https://github.com/NEO-SH1W4/docsync/discussions)**

</div>
