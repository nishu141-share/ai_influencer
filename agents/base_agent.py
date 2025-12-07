import abc
import yaml
import os
from typing import Any, Dict, Optional

class AgentBase(abc.ABC):
    """
    Abstract base class for all agents in the AI Influencer system.
    """
    def __init__(self, name: str, config_path: Optional[str] = None):
        self.name = name
        self.config = self._load_config(config_path) if config_path else {}
        print(f"[{self.name}] Initialized.")

    def _load_config(self, path: str) -> Dict[str, Any]:
        """Loads configuration from a YAML file."""
        if not os.path.exists(path):
            print(f"[{self.name}] Warning: Config file {path} not found.")
            return {}
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    @abc.abstractmethod
    def run(self, input_data: Any) -> Any:
        """
        Main execution method for the agent.
        Must be implemented by subclasses.
        """
        pass

    def log(self, message: str):
        """Standardized logging."""
        print(f"[{self.name}] {message}")
