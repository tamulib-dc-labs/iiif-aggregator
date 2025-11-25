import yaml
from pathlib import Path
from iiif_prezi3 import Collection


class IIIFAggregator:
    def __init__(self, config_path="config/config.yml", output_dir="collections", base_url=None):
        self.config_path = Path(config_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.base_url = base_url or "https://tamulib-dc-labs.github.io/iiif-aggregator/collections"
        self.config = self._load_config()
        self.groups = self.config["groups"]
        self.collections_data = self.config["collections"]
        self.root_collection = self._create_collection("collections", "Texas A&M Digital Collections", summary="All cultural heritage collections from TAMU")

    def _load_config(self):
        with open(self.config_path, "r") as f:
            return yaml.safe_load(f)

    def _create_collection(self, id_suffix, label, summary):
        """Create a IIIF Collection object."""
        return Collection(
            id=f"{self.base_url}/{id_suffix}.json",
            label=label,
            summary=summary
        )

    def _add_member_references(self, sub_collection, members):
        """Add member collection references to a sub-collection."""
        for member in members:
            info = self.collections_data[member]
            sub_collection.make_collection_ref(
                id=info["iiif_collection"].strip(),
                label=info["name"].strip(),
                summary=info["summary"].strip(),
                thumbnail=[
                    {"id": info["thumbnail"].strip(), "type": "Image"}
                ]
            )

    def _save_collection(self, collection, filename):
        """Write a collection JSON to disk."""
        with open(self.output_dir / filename, "w") as f:
            f.write(collection.json(indent=4))

    def build_collections(self):
        """Build all group collections and save them."""
        for group_key, details in self.groups.items():
            members = details.get("members", [])
            if not members:
                continue

            self.root_collection.make_collection_ref(
                id=f"{self.base_url}/{group_key}.json",
                label=details["name"],
                summary=details["summary"],
                thumbnail=[
                    {
                        "id": details["thumbnail"].strip(),
                        "type": "Image"
                    }
                ]
            )

            sub = self._create_collection(group_key, details["name"], details["summary"])
            self._add_member_references(sub, members)
            self._save_collection(sub, f"{group_key}.json")

        self._save_collection(self.root_collection, "collections.json")


if __name__ == "__main__":
    aggregator = IIIFAggregator()
    aggregator.build_collections()
