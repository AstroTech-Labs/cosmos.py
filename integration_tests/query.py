import asyncio
import base64
from pathlib import Path

from cosmos_sdk.client.lcd import LCDClient
from cosmos_sdk.core import Coins
from cosmos_sdk.core.bank import MsgSend
from cosmos_sdk.util.contract import get_code_id


def main():
    terra = LCDClient(
        url="https://pisco-lcd.terra.dev/",
        chain_id="pisco-1",
    )

    result = terra.tx.tx_infos_by_height(None)
    print(result)


main()
