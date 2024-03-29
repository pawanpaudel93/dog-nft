from scripts.helpful_scripts import (
    get_account,
    get_contract,
    OPENSEA_URL,
    fund_with_link,
)
from brownie import AdvancedCollectible, network, config


def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )
    fund_with_link(advanced_collectible.address, account)
    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("NFT has been created")
    return advanced_collectible, creating_tx


def main():
    deploy_and_create()
