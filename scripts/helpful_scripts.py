from brownie import (
    network,
    accounts,
    config,
    Contract,
    LinkToken,
    VRFCoordinatorMock,
    MockV3Aggregator,
    interface,
)

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
DECIMALS = 8
STARTING_PRICE = 2000 * 10 ** DECIMALS
LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "hardhat",
    "development",
    "ganache",
    "mainnet-fork",
    "binance-fork",
    "matic-fork",
]
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}

contract_to_mock = {
    # "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


def deploy_mocks(decimals=DECIMALS, starting_price=STARTING_PRICE):
    # MockV3Aggregator.deploy(decimals, starting_price, {"from": get_account()})
    link_token = LinkToken.deploy({"from": get_account()})
    VRFCoordinatorMock.deploy(link_token.address, {"from": get_account()})
    print("Mocks Deployed!")


def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config if defined, otherwise it will deploy the mock version of that contract and return the mock contract.
    Args:
        contract_name (string)
    Returns:
        brownie.network.contract.ProjectContract: The most recently deployed version of the contract.
    """
    contract_type = contract_to_mock.get(contract_name)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def fund_with_link(
    contract_address, account=None, link_token=None, amount=10 ** 17
):  # 0.1 LINK
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    # link_token = interface.LinkTokenInterface(link_token.address)
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print(f"Funded {contract_address}")
    return tx


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]
