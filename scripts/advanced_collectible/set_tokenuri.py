from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_account, OPENSEA_URL
import json
from pathlib import Path


def main():
    print("Working on {}".format(network.show_active()))
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_collectibles} collectibles")
    metadata_path = "./metadata/{}/metadata.json".format(network.show_active())
    if Path(metadata_path).exists():
        with open(
            "./metadata/{}/metadata.json".format(network.show_active()), "r"
        ) as fp:
            metadatas = json.load(fp)
        for token_id in range(number_of_collectibles):
            if not advanced_collectible.tokenURI(token_id).startswith("https://"):
                print(f"Setting tokenURI for {token_id}:")
                set_token_uri(
                    token_id,
                    advanced_collectible,
                    metadatas[str(token_id)],
                )
    else:
        print(f"No metadata file found at {metadata_path}")
        print("Please run create_metadata.py first")


def set_token_uri(token_id, nft_contract, token_uri):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, token_uri, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait upto 20 minutes, and hit the refresh metadata button")
