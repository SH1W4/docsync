"""Processador de documentação com recursos de IA para o sistema DOCSYNC.
Fornece análise, sugestões e melhorias para documentação técnica.
"""

import contextlib
import hashlib
import json
import logging
import os
import re
import time
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import yaml
from watchdog.events import FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer


class DocumentProcessor:
    """Processador principal de documentos com recursos de IA."""

    def __init__(self, config_path: Optional[Path] = None, cache_ttl: int = 3600) -> None:
        """Inicializa o processador de documentos."""
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config(config_path)
        self.cache: Dict[str, Tuple[float, Any]] = {}  # path -> (timestamp, data)
        self.cache_ttl = cache_ttl
        self.cache_lock = Lock()
        self.history = []
        self.stats = {
            "processed_files": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "errors": 0,
        }

    def _load_config(self, config_path: Optional[Path]) -> dict:
        """Carrega configurações do processador."""
        default_config = {
            "analysis_enabled": True,
            "suggestion_threshold": 0.7,
            "cache_ttl": 3600,
            "max_suggestions": 5,
            "languages": ["pt_BR", "en"],
            "doc_types": ["technical", "api", "architecture"],
        }

        if config_path and config_path.exists():
            with open(config_path, encoding="utf-8") as f:
                custom_config = yaml.safe_load(f)
                return {**default_config, **custom_config}
        return default_config

    def process_file(self, file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """Processa um arquivo com cache e extração de metadados."""
        try:
            file_path_str = str(file_path)
            current_time = time.time()

            # Verificar cache
            with self.cache_lock:
                if file_path_str in self.cache:
                    timestamp, data = self.cache[file_path_str]
                    if current_time - timestamp < self.cache_ttl:
                        self.stats["cache_hits"] += 1
                        return data
                self.stats["cache_misses"] += 1

            # Processar com base na extensão
            if file_path_str.endswith(".md"):
                result = self._process_markdown(file_path_str)
                result["type"] = "markdown"
            elif file_path_str.endswith((".yaml", ".yml")):
                result = self._process_yaml(file_path_str)
                result["type"] = "yaml"
            else:
                return None

            # Analisar se for markdown (AI features)
            if file_path_str.endswith(".md"):
                analysis = self.analyze_document(Path(file_path_str))
                result["analysis"] = analysis

            # Atualizar cache
            with self.cache_lock:
                self.cache[file_path_str] = (current_time, result)

            self.stats["processed_files"] += 1
            return result

        except Exception as e:
            self.stats["errors"] += 1
            msg = f"Error processing {file_path}: {e!s}"
            self.logger.error(msg)
            raise Exception(msg)

    def analyze_document(self, doc_path: Path) -> dict:
        """Analisa documento e fornece insights."""
        try:
            content = doc_path.read_text(encoding="utf-8")
            metadata, body = self._extract_metadata(content)

            analysis = {
                "metadata": metadata,
                "stats": self._analyze_stats(body),
                "quality": self._assess_quality(body),
                "suggestions": self._generate_suggestions(body, metadata),
                "timestamp": datetime.now().isoformat(),
            }

            return analysis

        except Exception as e:
            self.logger.exception(f"Erro ao analisar documento: {e}")
            raise

    def _extract_metadata(self, content: str) -> tuple[dict, str]:
        """Extrai e valida metadados do documento."""
        try:
            parts = content.split("---")
            if len(parts) >= 3:
                metadata = yaml.safe_load(parts[1]) or {}
                body = "---".join(parts[2:]).strip()
            else:
                metadata = {}
                body = content

            return metadata, body

        except Exception as e:
            self.logger.exception(f"Erro ao extrair metadados: {e}")
            return {}, content

    def _analyze_stats(self, content: str) -> dict:
        """Analisa estatísticas do documento."""
        words = content.split()
        sentences = content.split(".")

        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_sentence_length": len(words) / len(sentences) if sentences else 0,
            "sections": content.count("#"),
            "code_blocks": content.count("```"),
        }

    def _assess_quality(self, content: str) -> dict:
        """Avalia qualidade do documento."""
        quality_metrics = {
            "completeness": self._check_completeness(content),
            "clarity": self._analyze_clarity(content),
            "structure": self._evaluate_structure(content),
            "code_quality": self._check_code_quality(content),
        }

        return {
            "metrics": quality_metrics,
            "score": sum(quality_metrics.values()) / len(quality_metrics),
            "timestamp": datetime.now().isoformat(),
        }

    def _check_completeness(self, content: str) -> float:
        """Verifica completude do documento."""
        required_sections = ["# ", "## ", "Example", "Usage"]
        present_sections = sum(1 for section in required_sections if section in content)
        return present_sections / len(required_sections)

    def _analyze_clarity(self, content: str) -> float:
        """Analisa clareza do documento."""
        words = content.split()
        if not words:
            return 1.0
        complex_words = len([w for w in words if len(w) > 12])
        clarity_score = 1 - (complex_words / len(words))
        return min(max(clarity_score, 0), 1)

    def _evaluate_structure(self, content: str) -> float:
        """Avalia estrutura do documento."""
        lines = content.split("\n")
        section_levels = [line.count("#") for line in lines if line.startswith("#")]

        if not section_levels:
            return 0.0

        is_hierarchical = all(
            a <= b for a, b in zip(section_levels, section_levels[1:])
        )
        has_title = 1 in section_levels
        has_subsections = len(set(section_levels)) > 1

        return sum([is_hierarchical, has_title, has_subsections]) / 3

    def _check_code_quality(self, content: str) -> float:
        """Avalia qualidade dos blocos de código."""
        code_blocks = content.split("```")[1::2]
        if not code_blocks:
            return 1.0

        metrics = []
        for block in code_blocks:
            lines = [l for l in block.split("\n") if l.strip()]
            if len(lines) > 1:
                indents = {len(l) - len(l.lstrip()) for l in lines}
                indentation_consistent = len(indents) <= 3
                metrics.append(1.0 if indentation_consistent else 0.5)

            has_comments = any(line.strip().startswith(("#", "//", "/*")) for line in lines)
            metrics.append(1.0 if has_comments else 0.7)

        return sum(metrics) / len(metrics) if metrics else 1.0

    def _generate_suggestions(self, content: str, metadata: dict) -> list[dict]:
        """Gera sugestões de melhoria para o documento."""
        suggestions = []

        if not metadata.get("title"):
            suggestions.append({
                "type": "metadata",
                "severity": "high",
                "message": "Adicionar título ao documento",
                "context": "Metadados incompletos",
            })

        if not metadata.get("version"):
            suggestions.append({
                "type": "metadata",
                "severity": "medium",
                "message": "Especificar versão do documento",
                "context": "Controle de versão",
            })

        if not content.startswith("# "):
            suggestions.append({
                "type": "structure",
                "severity": "high",
                "message": "Iniciar documento com título principal (h1)",
                "context": "Estrutura do documento",
            })

        common_sections = ["## Overview", "## Installation", "## Usage", "## Examples"]
        missing_sections = [s for s in common_sections if s.lower() not in content.lower()]

        if missing_sections:
            suggestions.append({
                "type": "content",
                "severity": "medium",
                "message": f'Considerar adicionar seções: {", ".join(missing_sections)}',
                "context": "Completude do documento",
            })

        return suggestions[: self.config.get("max_suggestions", 5)]

    def _process_markdown(self, file_path: str) -> dict:
        """Extrai estrutura básica de markdown."""
        content = Path(file_path).read_text(encoding="utf-8")
        metadata, _ = self._extract_metadata(content)
        
        headers = []
        for line in content.split("\n"):
            if line.startswith("#"):
                level = len(line) - len(line.lstrip("#"))
                text = line.lstrip("#").strip()
                headers.append({"level": level, "text": text})

        code_blocks = []
        code_pattern = re.compile(r"```(\w+)?\n(.*?)\n```", re.DOTALL)
        for match in code_pattern.finditer(content):
            lang, code = match.groups()
            code_blocks.append({"language": lang or "text", "code": code.strip()})

        return {
            "metadata": metadata,
            "headers": headers,
            "code_blocks": len(code_blocks),
            "file_path": file_path,
            "last_modified": os.path.getmtime(file_path),
        }

    def _process_yaml(self, file_path: str) -> dict:
        """Processa arquivos YAML."""
        with open(file_path, encoding="utf-8") as f:
            content = yaml.safe_load(f)

        def analyze_structure(data, path="root"):
            if isinstance(data, dict):
                return {
                    "type": "dict",
                    "keys": list(data.keys()),
                    "nested": {k: analyze_structure(v, f"{path}.{k}") for k, v in data.items()},
                }
            if isinstance(data, list):
                return {
                    "type": "list",
                    "length": len(data),
                    "sample": analyze_structure(data[0], f"{path}[0]") if data else None,
                }
            return {"type": type(data).__name__, "path": path}

        return {
            "content": content,
            "structure": analyze_structure(content),
            "file_path": file_path,
            "last_modified": os.path.getmtime(file_path),
        }

    def get_stats(self) -> dict:
        """Retorna estatísticas de processamento."""
        return self.stats.copy()

    def process_directory(self, dir_path: Path) -> dict[str, dict]:
        """Processa todos os documentos em um diretório."""
        results = {}
        for doc_path in Path(dir_path).glob("**/*.md"):
            try:
                results[str(doc_path)] = self.process_file(doc_path)
            except Exception as e:
                results[str(doc_path)] = {"error": str(e)}
        return results

    def export_analysis(self, analysis: dict, output_path: Path) -> None:
        """Exporta resultados da análise."""
        output = {
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis,
            "config_version": self.config.get("version", "1.0"),
        }
        Path(output_path).write_text(json.dumps(output, indent=2), encoding="utf-8")


# Alias para compatibilidade com testes legados
DocProcessor = DocumentProcessor


class AIEnhancedMonitor(FileSystemEventHandler):
    """Monitor de arquivos inteligente com detecção de padrões."""

    def __init__(
        self,
        processor: Optional[DocumentProcessor] = None,
        patterns: Optional[Union[Set[str], List[str]]] = None,
        ignore_patterns: Optional[Union[Set[str], List[str]]] = None,
    ) -> None:
        self.processor = processor or DocumentProcessor()
        self.patterns = set(patterns) if patterns else {".md", ".yaml", ".yml"}
        self.ignore_patterns = set(ignore_patterns) if ignore_patterns else set()
        self.file_history: Dict[str, List[float]] = {}
        self.stats = {
            "events_processed": 0,
            "files_monitored": 0,
            "patterns_detected": set(),
        }
        self._lock = Lock()

    def on_modified(self, event: FileModifiedEvent) -> None:
        """Trata eventos de modificação de arquivo."""
        if not event.is_directory and self._should_process(event.src_path):
            with self._lock:
                self.stats["events_processed"] += 1
                path = event.src_path
                current_time = time.time()
                
                if path not in self.file_history:
                    self.file_history[path] = []
                    self.stats["files_monitored"] += 1

                self.file_history[path].append(current_time)
                self.file_history[path] = [t for t in self.file_history[path] if current_time - t < 3600]

                if len(self.file_history[path]) >= 1:
                    ext = Path(path).suffix[1:].lower()
                    pattern_map = {"md": "markdown", "yaml": "yaml", "yml": "yaml"}
                    detected = pattern_map.get(ext, ext)
                    self.stats["patterns_detected"].add(detected)

                with contextlib.suppress(Exception):
                    self.processor.process_file(path)

    def _should_process(self, path: str) -> bool:
        """Verifica se o arquivo deve ser processado."""
        path_str = str(path)
        # Check ignore patterns (handling both glob-like and extension-like)
        if any(path_str.endswith(pat) or Path(path_str).match(pat) for pat in self.ignore_patterns):
            return False
        # Check include patterns
        return any(path_str.endswith(pat) or Path(path_str).match(pat) for pat in self.patterns)

    def get_stats(self) -> dict:
        """Retorna estatísticas de monitoramento."""
        with self._lock:
            stats = self.stats.copy()
            stats["processor_stats"] = self.processor.get_stats()
            return stats


def setup_monitoring(
    path: str,
    patterns: Optional[Set[str]] = None,
) -> Tuple[Observer, AIEnhancedMonitor]:
    """Configura o monitoramento de arquivos para um diretório."""
    processor = DocumentProcessor()
    monitor = AIEnhancedMonitor(processor, patterns)
    observer = Observer()
    observer.schedule(monitor, path, recursive=True)
    observer.start()
    return observer, monitor
