from brownie import network
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    # Arrange
    account = get_account()
    # Act
    advanced_collectible, creation_tx = deploy_and_create()
    request_id = creation_tx.events["requestedCollectible"]["requestId"]
    randomness = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, randomness, advanced_collectible.address, {"from": account}
    )
    # Assert
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == randomness % 3
