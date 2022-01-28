import os
import requests
from pathlib import Path

PINATA_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"


filepath = "./img/pug.png"
filename = filepath.split("/")[-1]
headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}


def main():
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_URL, headers=headers, files={"file": (filename, image_binary)}
        )
        ipfs_hash = response.json()["IpfsHash"]
        print(ipfs_hash)
