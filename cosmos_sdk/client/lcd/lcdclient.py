from __future__ import annotations

from asyncio import AbstractEventLoop, get_event_loop
from json import JSONDecodeError
from typing import List, Optional, Union

import nest_asyncio
from aiohttp import ClientSession
from multidict import CIMultiDict

from cosmos_sdk.core import Coins, Dec, Numeric
from cosmos_sdk.exceptions import LCDResponseError
from cosmos_sdk.key.key import Key
from cosmos_sdk.util.json import dict_to_data
from cosmos_sdk.util.url import urljoin

from .api.auth import AsyncAuthAPI, AuthAPI
from .api.authz import AsyncAuthzAPI, AuthzAPI
from .api.bank import AsyncBankAPI, BankAPI
from .api.distribution import AsyncDistributionAPI, DistributionAPI
from .api.feegrant import AsyncFeeGrantAPI, FeeGrantAPI
from .api.gov import AsyncGovAPI, GovAPI
from .api.ibc import AsyncIbcAPI, IbcAPI
from .api.ibc_transfer import AsyncIbcTransferAPI, IbcTransferAPI
from .api.mint import AsyncMintAPI, MintAPI
from .api.slashing import AsyncSlashingAPI, SlashingAPI
from .api.staking import AsyncStakingAPI, StakingAPI
from .api.tendermint import AsyncTendermintAPI, TendermintAPI
from .api.tx import AsyncTxAPI, TxAPI
from .api.wasm import AsyncWasmAPI, WasmAPI
from .lcdutils import AsyncLCDUtils, LCDUtils
from .params import APIParams
from .wallet import AsyncWallet, Wallet


def get_default(chain_id: str) -> [Coins, Numeric]:
    if chain_id == "phoenix-1":     # TERRA 2 MAINNET
        return [Coins.from_str("0.15uluna"), Numeric.parse(1.75)]
    if chain_id == "pisco-1":       # TERRA 2 TESTNET
        return [Coins.from_str("0.15uluna"), Numeric.parse(1.75)]
    if chain_id == "localterra":    # TERRA 2 LOCALNET
        return [Coins.from_str("0.15uluna"), Numeric.parse(1.75)]
    if chain_id == "juno-1":    # JUNO MAINNET
        return [Coins.from_str("0.15ujuno"), Numeric.parse(1.75)]
    if chain_id == "kaiyo-1":    # KUJIRA MAINNET
        return [Coins.from_str("0.15ukuji"), Numeric.parse(1.75)]
    if chain_id == "core-1":    # PERSISTENCE MAINNET
        return [Coins.from_str("0.15uxprt"), Numeric.parse(1.75)]
    if chain_id == "test-core-1":    # PERSISTENCE TESTNET
        return [Coins.from_str("0.15uxprt"), Numeric.parse(1.75)]
    if chain_id == "testing":    # PERSISTENCE LOCALNET
        return [Coins.from_str("0.15uxprt"), Numeric.parse(1.75)]
    if chain_id == "osmosis-1":    # OSMOSIS MAINNET
        return [Coins.from_str("0.15uosmo"), Numeric.parse(1.75)]


    raise ValueError("chain_id is invalid")


class AsyncLCDClient:
    def __init__(
        self,
        url: str,
        chain_id: Optional[str] = None,
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
        loop: Optional[AbstractEventLoop] = None,
        _create_session: bool = True,  # don't create a session (used for sync LCDClient)
    ):
        if loop is None:
            loop = get_event_loop()
        self.loop = loop
        if _create_session:
            self.session = ClientSession(
                headers={"Accept": "application/json"}, loop=self.loop
            )

        self.chain_id = chain_id
        self.url = url
        self.last_request_height = None

        default_price, default_adjustment = get_default(chain_id)
        self.gas_prices = Coins(gas_prices) if gas_prices else default_price
        self.gas_adjustment = gas_adjustment if gas_adjustment else default_adjustment

        self.auth = AsyncAuthAPI(self)
        self.bank = AsyncBankAPI(self)
        self.distribution = AsyncDistributionAPI(self)
        self.feegrant = AsyncFeeGrantAPI(self)
        self.gov = AsyncGovAPI(self)
        self.mint = AsyncMintAPI(self)
        self.authz = AsyncAuthzAPI(self)
        self.slashing = AsyncSlashingAPI(self)
        self.staking = AsyncStakingAPI(self)
        self.tendermint = AsyncTendermintAPI(self)
        self.wasm = AsyncWasmAPI(self)
        self.ibc = AsyncIbcAPI(self)
        self.ibc_transfer = AsyncIbcTransferAPI(self)
        self.tx = AsyncTxAPI(self)
        self.utils = AsyncLCDUtils(self)

    def wallet(self, key: Key) -> AsyncWallet:
        """Creates a :class:`AsyncWallet` object from a key.

        Args:
            key (Key): key implementation
        """
        return AsyncWallet(self, key)

    async def _get(
        self,
        endpoint: str,
        params: Optional[Union[APIParams, CIMultiDict, list, dict]] = None,
        # raw: bool = False
    ):
        if (
            params
            and hasattr(params, "to_dict")
            and callable(getattr(params, "to_dict"))
        ):
            params = params.to_dict()

        async with self.session.get(
            urljoin(self.url, endpoint), params=params
        ) as response:
            try:
                result = await response.json(content_type=None)
            except JSONDecodeError:
                raise LCDResponseError(message=str(response.reason), response=response)
            if not 200 <= response.status < 299:
                raise LCDResponseError(message=str(result), response=response)
        self.last_request_height = (
            result.get("height") if result else self.last_request_height
        )
        return result  # if raw else result["result"]

    async def _post(
        self, endpoint: str, data: Optional[dict] = None  # , raw: bool = False
    ):
        async with self.session.post(
            urljoin(self.url, endpoint), json=data and dict_to_data(data)
        ) as response:
            try:
                result = await response.json(content_type=None)
            except JSONDecodeError:
                raise LCDResponseError(message=str(response.reason), response=response)
            if not 200 <= response.status < 299:
                raise LCDResponseError(message=result.get("message"), response=response)
        self.last_request_height = (
            result.get("height") if result else self.last_request_height
        )
        return result  # if raw else result["result"]

    async def _search(
        self,
        events: List[list],
        params: Optional[Union[APIParams, CIMultiDict, list, dict]] = None,
        # raw: bool = False
    ):

        actual_params : CIMultiDict = CIMultiDict()

        for event in events:
            if event[0] == "tx.height":
                actual_params.add("events", f"{event[0]}={event[1]}")
            else:
                actual_params.add("events", f"{event[0]}='{event[1]}'")
        if params:
            for p in params:
                actual_params.add(p, params[p])

        async with self.session.get(
            urljoin(self.url, "/cosmos/tx/v1beta1/txs"), params=actual_params
        ) as response:
            try:
                result = await response.json(content_type=None)
            except JSONDecodeError:
                raise LCDResponseError(message=str(response.reason), response=response)
            if not 200 <= response.status < 299:
                raise LCDResponseError(message=str(result), response=response)
        self.last_request_height = (
            result.get("height") if result else self.last_request_height
        )
        return result  # if raw else result["result"]

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()


class LCDClient(AsyncLCDClient):
    """An object representing a connection to a node running the Terra LCD server."""

    url: str
    """URL endpoint of LCD server."""

    chain_id: str
    """Chain ID of blockchain network connecting to."""

    gas_prices: Coins.Input
    """Gas prices to use for automatic fee estimation."""

    gas_adjustment: Union[str, float, int, Dec]
    """Gas adjustment factor for automatic fee estimation."""

    last_request_height: Optional[int]  # type: ignore
    """Height of response of last-made made LCD request."""

    auth: AuthAPI
    """:class:`AuthAPI<cosmos_sdk.client.lcd.api.auth.AuthAPI>`."""

    bank: BankAPI
    """:class:`BankAPI<cosmos_sdk.client.lcd.api.bank.BankAPI>`."""

    distribution: DistributionAPI
    """:class:`DistributionAPI<cosmos_sdk.client.lcd.api.distribution.DistributionAPI>`."""

    gov: GovAPI
    """:class:`GovAPI<cosmos_sdk.client.lcd.api.gov.GovAPI>`."""

    feegrant: FeeGrantAPI
    """:class:`FeeGrant<cosmos_sdk.client.lcd.api.feegrant.FeeGrantAPI>`."""

    mint: MintAPI
    """:class:`MintAPI<cosmos_sdk.client.lcd.api.mint.MintAPI>`."""

    authz: AuthzAPI
    """:class:`AuthzAPI<cosmos_sdk.client.lcd.api.authz.AuthzAPI>`."""

    slashing: SlashingAPI
    """:class:`SlashingAPI<cosmos_sdk.client.lcd.api.slashing.SlashingAPI>`."""

    staking: StakingAPI
    """:class:`StakingAPI<cosmos_sdk.client.lcd.api.staking.StakingAPI>`."""

    tendermint: TendermintAPI
    """:class:`TendermintAPI<cosmos_sdk.client.lcd.api.tendermint.TendermintAPI>`."""

    wasm: WasmAPI
    """:class:`WasmAPI<cosmos_sdk.client.lcd.api.wasm.WasmAPI>`."""

    tx: TxAPI
    """:class:`TxAPI<cosmos_sdk.client.lcd.api.tx.TxAPI>`."""

    ibc: IbcAPI
    """:class:`IbcAPI<cosmos_sdk.client.lcd.api.ibc.IbcAPI>`."""

    ibc_transfer: IbcTransferAPI
    """:class:`IbcTransferAPI<cosmos_sdk.client.lcd.api.ibc_transfer.IbcTransferAPI>`."""

    def __init__(
        self,
        url: str,
        chain_id: str = None,
        gas_prices: Optional[Coins.Input] = None,
        gas_adjustment: Optional[Numeric.Input] = None,
    ):
        super().__init__(
            url,
            chain_id,
            gas_prices,
            gas_adjustment,
            _create_session=False,
            loop=nest_asyncio.apply(get_event_loop()),
        )

        self.auth = AuthAPI(self)
        self.bank = BankAPI(self)
        self.distribution = DistributionAPI(self)
        self.gov = GovAPI(self)
        self.feegrant = FeeGrantAPI(self)
        self.mint = MintAPI(self)
        self.authz = AuthzAPI(self)
        self.slashing = SlashingAPI(self)
        self.staking = StakingAPI(self)
        self.tendermint = TendermintAPI(self)
        self.wasm = WasmAPI(self)
        self.ibc = IbcAPI(self)
        self.ibc_transfer = IbcTransferAPI(self)
        self.tx = TxAPI(self)
        self.utils = LCDUtils(self)

    async def __aenter__(self):
        raise NotImplementedError(
            "async context manager not implemented - you probably want AsyncLCDClient"
        )

    async def __aexit__(self, exc_type, exc, tb):
        raise NotImplementedError(
            "async context manager not implemented - you probably want AsyncLCDClient"
        )

    def wallet(self, key: Key) -> Wallet:  # type: ignore
        """Creates a :class:`Wallet` object from a key for easy transaction creating and
        signing.

        Args:
            key (Key): key implementation
        """
        return Wallet(self, key)

    async def _get(self, *args, **kwargs):
        # session has to be manually created and torn down for each HTTP request in a
        # synchronous client
        self.session = ClientSession(
            headers={"Accept": "application/json"}, loop=self.loop
        )
        try:
            result = await super()._get(*args, **kwargs)
        finally:
            await self.session.close()
        return result

    async def _post(self, *args, **kwargs):
        # session has to be manually created and torn down for each HTTP request in a
        # synchronous client
        self.session = ClientSession(
            headers={"Accept": "application/json"}, loop=self.loop
        )
        try:
            result = await super()._post(*args, **kwargs)
        finally:
            await self.session.close()
        return result

    async def _search(self, *args, **kwargs):
        # session has to be manually created and torn down for each HTTP request in a
        # synchronous client
        self.session = ClientSession(
            headers={"Accept": "application/json"}, loop=self.loop
        )
        try:
            result = await super()._search(*args, **kwargs)
        finally:
            await self.session.close()
        return result
