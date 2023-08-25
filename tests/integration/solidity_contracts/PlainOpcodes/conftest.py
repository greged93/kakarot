import logging

import pytest_asyncio

from tests.utils.helpers import hex_string_to_bytes_array
from tests.utils.reporting import traceit

logger = logging.getLogger()


@pytest_asyncio.fixture(scope="session")
def counter_deployer(addresses):
    return addresses[1]


@pytest_asyncio.fixture(scope="session")
def caller_deployer(addresses):
    return addresses[2]


@pytest_asyncio.fixture(scope="session")
def plain_opcodes_deployer(addresses):
    return addresses[3]


@pytest_asyncio.fixture(scope="session")
def safe_deployer(addresses):
    return addresses[4]


@pytest_asyncio.fixture(scope="session")
def empty_deployer_one(addresses):
    return addresses[5]


@pytest_asyncio.fixture(scope="session")
def empty_deployer_two(addresses):
    return addresses[6]


@pytest_asyncio.fixture(scope="package")
async def counter(deploy_solidity_contract, counter_deployer):
    return await deploy_solidity_contract(
        "PlainOpcodes", "Counter", caller_eoa=counter_deployer
    )


@pytest_asyncio.fixture(scope="package")
async def caller(deploy_solidity_contract, caller_deployer):
    return await deploy_solidity_contract(
        "PlainOpcodes",
        "Caller",
        caller_eoa=caller_deployer,
    )


@pytest_asyncio.fixture(scope="package")
async def plain_opcodes(deploy_solidity_contract, plain_opcodes_deployer, counter):
    return await deploy_solidity_contract(
        "PlainOpcodes",
        "PlainOpcodes",
        counter.evm_contract_address,
        caller_eoa=plain_opcodes_deployer,
    )


@pytest_asyncio.fixture(scope="package")
async def safe(deploy_solidity_contract, safe_deployer):
    return await deploy_solidity_contract(
        "PlainOpcodes", "Safe", caller_eoa=safe_deployer
    )


@pytest_asyncio.fixture(scope="package")
async def empty_one(kakarot, empty_deployer_one):
    try:
        deploy_bytecode = hex_string_to_bytes_array("0x60006000f3")
        with traceit.context("empty"):
            tx = await kakarot.eth_send_transaction(
                to=0, gas_limit=1_000_000, gas_price=0, value=0, data=deploy_bytecode
            ).execute(caller_address=empty_deployer_one.starknet_address)

        deploy_event = [
            e
            for e in tx.main_call_events
            if type(e).__name__ == "evm_contract_deployed"
        ][0]
        return deploy_event
    except Exception as e:
        logger.error("in one")
        logger.error(e)


@pytest_asyncio.fixture(scope="package")
async def empty_two(kakarot, empty_deployer_two):
    try:
        deploy_bytecode = hex_string_to_bytes_array("0x60006000f3")
        with traceit.context("empty"):
            tx = await kakarot.eth_send_transaction(
                to=0, gas_limit=1_000_000, gas_price=0, value=0, data=deploy_bytecode
            ).execute(caller_address=empty_deployer_two.starknet_address)

        deploy_event = [
            e
            for e in tx.main_call_events
            if type(e).__name__ == "evm_contract_deployed"
        ][0]
        return deploy_event
    except Exception as e:
        logger.error("in two")
        logger.error(e)
