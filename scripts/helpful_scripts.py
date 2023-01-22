from brownie import (
    network, 
    config, 
    accounts, 
    Contract, 
    VRFCoordinatorMock,
    LinkToken,

)
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS =["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS =["mainnet-fork", "mainnet-fork-dev"]
OPENSEA_URL= "https://testnets.opensea.io/assets/{}/{}"

def get_account(index=None, id=None):

    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS 
    or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        print("Running brownie local account!")
        return accounts[0]
    else:
        print("Running on " + network.show_active() + "network.")
        return accounts.add(config['wallets']["from_key"])


def deploy_mocks():
    print(f"Deploying Mocks on {network.show_active()} network.")
    account = get_account()

    print("Deploying Mock LinkToken...")
    link_token=LinkToken.deploy({"from":account})
    print(f"Link Token deployed to {link_token.address}")

    print("Deploying VRFCoordinatorMock...")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token, {"from":account})
    print(f"VRFCoordinatorMock Mock deployed to {vrf_coordinator.address}\n")

contract_to_mock={
    "vrf_coordinator" : VRFCoordinatorMock,
    "link_token" : LinkToken,
}

def get_contract(contract_name):
    print("-> Getting contract {}...".format(contract_name))
    contract_type = contract_to_mock[contract_name]
    #print("contract_type {} {}".format(contract_type, len(contract_type)))

    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS) :
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        # Mainnet or Testnet i.e a real network
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi 
        )
    print(".")
    return contract

        
def fund_with_link(contract_address, 
        account=None, 
        link_token=None, 
        amount=100000000000000000):
    account=account if account else get_account()
    link_token=link_token if link_token else get_contract("link_token")
    tx=link_token.transfer(contract_address, amount, {"from": account})
    
    # Alternative to from_abi using interface
    # link_token_conttract=interface.LinkTokenInterface(link_token.address)
    # tx=link_token_conttract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Funded contract with link token.")
    return tx
