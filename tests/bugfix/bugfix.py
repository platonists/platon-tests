import asyncio
import pytest
import time
from platon_env.chain import Chain


@pytest.mark.asyncio
async def test_a():
    time.sleep(2)
    await asyncio.sleep(5)


@pytest.mark.asyncio
async def test_b():
    await asyncio.sleep(3)


def test_debug(aides):
    print(aides)
    print(aides[0].personal.new_account())
    aides[0].staking.create_staking()
    aides[0].transfer.transfer()
    aides[0].delegate._economic.staking_limit
    aides[0].delegate._economic.delegate_limit
    aides[0].platon.get_balance()
    aides[0].set_default_account()
    aides[0].staking.staking_info
    aides[0].staking.get_candidate_info()
    aides[0].delegate.delegate
    aides[0].delegate.get_delegate_info()
    aides[0].web3.to_checksum_address()
    aides[0].platon.block_number
    aides[0].wait_block()
    aides[0].staking.get_verifier_list()
    aides[0].staking.get_validator_list()
    aides[0].staking.withdrew_staking()
    aides[0].uri
    aides[0].delegate.get_delegate_list()
    aides[0].web3.toVon()
    aides[0].web3.restricting.create_restricting()
    aides[0].web3.restricting.get_restricting_info()

    aides[0].graphql.execute()
    aides[0].platon.get_block(0)
    aides[0].platon.filter

    aides[0].txpool.status()
    aides[0].platon.gas_price()
    aides[0].web3.chain_id()
    aides[0].web3.to_bech32_address()
