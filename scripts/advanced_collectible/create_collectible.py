from brownie import AdvancedCollectible
from scripts.helpful_scripts import fund_with_link, get_account
from web3 import Web3


def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(
        advanced_collectible.address, account, amount=Web3.toWei(0.1, "ether")
    )
    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("Collectible created")
