from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import SimpleCollectible

sample_token_uri = "https://ipfs.io/ipfs/QmSEDJ7zbD2QVAchf8QCEbLTCtebK713veCiz1eLZCibhE?filename=0-PUG.json"


def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx = simple_collectible.createCollectible(sample_token_uri, {"from": account})
    tx.wait(1)
    print(
        f"Awesome, you can view your NFT at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter()-1)}"
    )
    print("Please wait upto 20 minutes, and hit refresh metadata button.")
    return simple_collectible


def main():
    deploy_and_create()
