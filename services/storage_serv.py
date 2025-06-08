import json
import os
from datetime import datetime
from pathlib import Path
import uuid

class GraphStorage:
    def __init__(self):
        self.storage_dir = Path("graph_storage")
        self.data_file = self.storage_dir / "graphs_data.json"
        self.ensure_storage()

    def ensure_storage(self):
        self.storage_dir.mkdir(exist_ok=True)
        if not self.data_file.exists():
            with open(self.data_file, 'w') as f:
                json.dump({}, f)

    def save_graph(self, formula: str, image_data: bytes) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"graph_{timestamp}_{uuid.uuid4().hex[:6]}.png"
        filepath = self.storage_dir / filename

        with open(filepath, 'wb') as f:
            f.write(image_data)

        data = self.load_data()
        data[formula] = str(filepath)
        self.save_data(data)

        return str(filepath)

    def load_data(self) -> dict:
        with open(self.data_file, 'r') as f:
            return json.load(f)

    def save_data(self, data: dict):
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)

    def get_graph_path(self, formula: str) -> str:
        data = self.load_data()
        return data.get(formula)