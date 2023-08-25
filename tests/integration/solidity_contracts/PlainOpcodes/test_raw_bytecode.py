import logging

import pytest
from starkware.starknet.testing.contract import StarknetContract
from starkware.starknet.testing.contract_utils import gather_deprecated_compiled_class
from starkware.starknet.testing.starknet import Starknet

from tests.utils.helpers import hex_string_to_bytes_array

logger = logging.getLogger()


@pytest.mark.asyncio
@pytest.mark.EF_TEST
class TestSafe:
    async def test_should_deploy_contract_account_and_call_with_bytecode(
        self, owner, kakarot: StarknetContract, starknet: Starknet, empty_one, empty_two
    ):

        logger.info(empty_one)
        logger.info(empty_two)
        try:
            contract_class = gather_deprecated_compiled_class(
                source="./src/kakarot/accounts/contract/contract_account.cairo",
                cairo_path=["src"],
                disable_hint_validation=True,
            )
            contract = StarknetContract(
                starknet.state,
                contract_class.abi,
                empty_one.starknet_contract_address,
                None,
            )
            await contract.write_bytecode(
                hex_string_to_bytes_array("0x600060002060005500")
            ).execute(caller_address=kakarot.contract_address)

            executor = StarknetContract(
                starknet.state,
                contract_class.abi,
                empty_two.starknet_contract_address,
                None,
            )
            await executor.write_bytecode(
                hex_string_to_bytes_array(
                    "0x604060206010600f6000600435610100016001600003f100"
                )
            ).execute(caller_address=kakarot.contract_address)

            await kakarot.eth_send_transaction(
                to=empty_two.evm_contract_address,
                gas_limit=1_000_000,
                gas_price=0,
                value=0,
                data=hex_string_to_bytes_array(
                    "0x693c6139000000000000000000000000"
                    + hex(empty_one.evm_contract_address - 256)[2:].zfill(40)
                ),
                origin=empty_two.evm_contract_address,
            ).execute(caller_address=owner.starknet_address)
        except Exception as e:
            logger.error("in main")
            logger.error(e)
