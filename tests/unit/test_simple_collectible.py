from scripts.simple_collectible.deploy_and_create import deploy_and_create
from scripts.helpful_scripts import get_account
import pytest
from brownie import network

LOCAL_BLOCKCHAIN_ENVIRONMENTS =["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS =["mainnet-fork", "mainnet-fork-dev"]
def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    simple_collectible = deploy_and_create()
    assert simple_collectible.ownerOf()==get_account()
