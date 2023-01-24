from scripts.helpful_scripts import get_account, get_contract, fund_with_link, OPENSEA_URL
from brownie import AdvancedCollectible, config, network

sample_token_uri = "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"

def deploy_and_create():
    account=get_account()
    print("--------AdvancedCollectible-------------")
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account}
    )
    print("---------fund_with_link------------")
    funding_tx = fund_with_link(advanced_collectible.address)
    print("---------createCollectible------------")
    network.gas_limit(6700000)
    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New token has been created.")

def call():
    advanced_collectible =  get_contract("vrf_coordinator")
def main():
    deploy_and_create()