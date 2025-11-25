import yaml
from iiif_prezi3 import Collection

with open("config/config.yml", "r") as f:
    data = yaml.safe_load(f)

groups = data["groups"]
collections = data["collections"]
parent = data["parent"]


collection = Collection(
    id = "https://tamulib-dc-labs.github.io/iiif-aggregator/collections/collections.json",
    label = "Texas A&M Digital Collections",
    type = "Collection"
)
for group, details in groups.items():
    if len(details["members"]) > 0:
        collection.make_collection_ref(
            id=f"https://tamulib-dc-labs.github.io/iiif-aggregator/collections/{group}.json",
            label=details["name"],
            type="Collection"
        )
        sub_collection = Collection(
            id=f"https://tamulib-dc-labs.github.io/iiif-aggregator/collections/{group}.json",
            label=details["name"],
            type="Collection"
        )
        for member in details["members"]:
            sub_collection.make_collection_ref(
                id=collections[member]['iiif_collection'].strip(),
                label=collections[member]['name'].strip(),
                summary=collections[member]['summary'].strip(),
                # @todo: Thumbnail should be handled better
                thumbnail=[
                    {
                        "id": collections[member]['thumbnail'].strip(),
                        "type": "Image"
                    }
                ]
            )
        with open(f"collections/{group}.json", "w") as f:
            f.write(sub_collection.json(indent=4))
with open(f"collections/collections.json", "w") as f:
    f.write(collection.json(indent=4))