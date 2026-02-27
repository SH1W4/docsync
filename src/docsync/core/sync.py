"""Implementação principal do DocSync."""

import logging
from pathlib import Path
from typing import Optional, Union

from rich.console import Console
from rich.logging import RichHandler

from docsync.utils.config import load_config


class DocSync:
    """Sistema de sincronização de documentação."""

    def __init__(
        self,
        base_path: Union[str, Path],
        config_path: Optional[Union[str, Path]] = None,
    ) -> None:
        """Inicializa o DocSync.

        Args:
            base_path: Diretório base da documentação
            config_path: Caminho opcional para arquivo de configuração
        """
        self.base_path = Path(base_path).resolve()
        self.console = Console()
        self.logger = logging.getLogger("docsync")
        
        # Procura configuração se não for fornecida
        if config_path:
            self.config_path = Path(config_path)
        else:
            # Tenta encontrar docsync.yaml ou docsync.yml no diretório base
            yaml_path = self.base_path / "docsync.yaml"
            yml_path = self.base_path / "docsync.yml"
            if yaml_path.exists():
                self.config_path = yaml_path
            elif yml_path.exists():
                self.config_path = yml_path
            else:
                self.config_path = None

        # Configurar logging
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            handler = RichHandler(console=self.console)
            handler.setFormatter(logging.Formatter("%(message)s"))
            self.logger.addHandler(handler)

        # Carregar configuração
        self.config = load_config(self.config_path) if self.config_path else {}

        # Definir caminhos
        templates_dir = self.config.get("templates_path") or self.config.get("templates", {}).get("default_path", "templates")
        self.templates_path = self.base_path / templates_dir
        
        # Inicializar componentes (placeholder para satisfazer testes)
        from docsync.monitor import FileMonitor, MonitorConfig
        self.monitor = FileMonitor(MonitorConfig(paths=[self.base_path]))
        self.observer = self.monitor.observer

        # Criar diretório base se não existir
        self.base_path.mkdir(parents=True, exist_ok=True)

        self.logger.info("✨ DocSync inicializado em %s", self.base_path)

    def start_monitoring(self) -> None:
        """Inicia o monitoramento de arquivos."""
        self.monitor.start()

    def stop_monitoring(self) -> None:
        """Para o monitoramento de arquivos."""
        self.monitor.stop()

    def create_document(self, template_name: str, target_path: Path, **kwargs) -> None:
        """Cria um novo documento a partir de um template."""
        from docsync.utils.renderer import ReportRenderer
        renderer = ReportRenderer(str(self.templates_path))
        content = renderer.render(f"{template_name}.md", kwargs)
        
        target_path = Path(target_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding="utf-8")
        self.logger.info("📄 Documento criado em %s", target_path)

    def sync_documents(self) -> None:
        """Sincroniza documentos (placeholder)."""
        self.logger.info("🔄 Sincronizando documentos...")
