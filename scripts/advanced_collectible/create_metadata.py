import requests
import json
from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles")
    metadata_path = "./metadata/{}/metadata.json".format(network.show_active())
    if Path(metadata_path).exists():
        with Path(metadata_path).open("r") as fp:
            metadatas = json.load(fp)
    else:
        metadatas = {}
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_filename = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_filename).exists():
            print(
                f"Metadata for {metadata_filename} already exists! Delete it to overwrite."
            )
        else:
            print(f"Creating metadata for {metadata_filename}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            image_path = "./img/{}.png".format(breed.lower().replace("_", "-"))
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["image"] = image_uri
            with open(metadata_filename, "w") as fp:
                json.dump(collectible_metadata, fp, indent=4)
            file_uri = upload_to_ipfs(metadata_filename)
            metadatas[token_id] = file_uri
    with open(f"./metadata/{network.show_active()}/metadata.json", "w") as fp:
        json.dump(metadatas, fp, indent=4)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        file_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": file_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1]
        file_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(file_uri)
        return file_uri
