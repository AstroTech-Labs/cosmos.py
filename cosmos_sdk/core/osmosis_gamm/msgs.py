"Osmosis GAMM module messages."

from __future__ import annotations

import json
from cProfile import label
from typing import Optional, Union

import attr
from betterproto.lib.google.protobuf import Any as Any_pb

from cosmos_proto.osmosis_proto.gamm.v1beta1 import MsgJoinPool as MsgJoinPool_pb
from cosmos_proto.osmosis_proto.gamm.v1beta1 import MsgExitPool as MsgExitPool_pb
from cosmos_proto.osmosis_proto.gamm.v1beta1 import MsgSwapExactAmountIn as MsgSwapExactAmountIn_pb
from cosmos_proto.osmosis_proto.gamm.v1beta1 import MsgSwapExactAmountOut as MsgSwapExactAmountOut_pb
from cosmos_proto.osmosis_proto.gamm.v1beta1 import MsgJoinSwapExternAmountIn as MsgJoinSwapExternAmountIn_pb
from cosmos_proto.osmosis_proto.gamm.v1beta1 import MsgJoinSwapShareAmountOut as MsgJoinSwapShareAmountOut_pb
from cosmos_proto.osmosis_proto.gamm.v1beta1 import MsgExitSwapExternAmountOut as MsgExitSwapExternAmountOut_pb
from cosmos_proto.osmosis_proto.gamm.v1beta1 import MsgExitSwapShareAmountIn as MsgExitSwapShareAmountIn_pb

from cosmos_sdk.core.osmosis_gamm.data import SwapAmountInRoute, SwapAmountOutRoute
from cosmos_sdk.core import AccAddress, Coins, Coin
from cosmos_sdk.core.msg import Msg
from cosmos_sdk.util.remove_none import remove_none

__all__ = [
    "MsgJoinPool",
    "MsgExitPool",
    "MsgSwapExactAmountIn",
    "MsgSwapExactAmountOut",
    "MsgJoinSwapExternAmountIn",
    "MsgJoinSwapShareAmountOut",
    "MsgExitSwapExternAmountOut",
    "MsgExitSwapShareAmountIn"
]


def parse_msg(msg: Union[dict, str, bytes]) -> dict:
    if type(msg) is dict:
        return msg
    return json.loads(msg)


@attr.s
class MsgJoinPool(Msg):
    """Join an OSMOSIS pool with the given token amounts.

    Args:
        sender: address of sender
        pool_id: id of the pool to join
        share_out_amount: amount of shares to receive
        token_in_maxs: maximum amounts of tokens to send
    """

    type_amino = "osmosis/Msg/JoinPool"
    """"""
    type_url = "/osmosis.gamm.v1beta1.Msg/JoinPool"
    """"""
    prototype = MsgJoinPool_pb
    """"""

    sender: AccAddress = attr.ib()
    pool_id: int = attr.ib()
    share_out_amount: str = attr.ib()
    token_in_maxs: Coins = attr.ib(converter=Coins, factory=Coins)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "pool_id": self.pool_id,
                "share_out_amount": self.share_out_amount(),
                "coins": self.token_in_maxs.to_amino(),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgJoinPool:
        return cls(
            sender=data["sender"],
            pool_id=data["pool_id"],
            share_out_amount=data["share_out_amount"],
            coins=Coins.from_data(data["funds"]),
        )

    def to_proto(self) -> MsgJoinPool_pb:
        return MsgJoinPool_pb(
            sender=self.sender,
            pool_id=self.pool_id,
            share_out_amount=self.share_out_amount,
            token_in_maxs=self.token_in_maxs.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: MsgJoinPool_pb) -> MsgJoinPool:
        return cls(
            sender=proto.sender,
            pool_id=proto.pool_id,
            share_out_amount=proto.share_out_amount,
            token_in_maxs=Coins.from_proto(proto.token_in_maxs)
        )


@attr.s
class MsgExitPool(Msg):
    """Exit an OSMOSIS pool with the given token amounts.

    Args:
        sender: address of sender
        pool_id: id of the pool to exit
        share_in_amount: amount of shares to send
        token_out_mins: minimum amounts of tokens to receive
    """

    type_amino = "osmosis/Msg/JoinPool"
    """"""
    type_url = "/osmosis.gamm.v1beta1.Msg/ExitPool"
    """"""
    prototype = MsgExitPool_pb
    """"""

    sender: AccAddress = attr.ib()
    pool_id: int = attr.ib()
    share_in_amount: str = attr.ib()
    token_out_mins: Coins = attr.ib(converter=Coins, factory=Coins)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "pool_id": self.pool_id,
                "share_in_amount": self.share_in_amount(),
                "coins": self.token_out_mins.to_amino(),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgExitPool:
        return cls(
            sender=data.get("sender"),
            pool_id=data.get("pool_id"),
            share_in_amount=data.get("share_in_amount"),
            coins=Coins.from_data(data.get("funds")),
        )

    def to_proto(self) -> MsgExitPool_pb:
        return MsgExitPool_pb(
            sender=self.sender,
            pool_id=self.pool_id,
            share_in_amount=self.share_in_amount,
            token_out_mins=self.token_out_mins.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: MsgExitPool_pb) -> MsgExitPool:
        return cls(
            sender=proto.sender,
            pool_id=proto.pool_id,
            share_in_amount=proto.share_in_amount,
            token_out_mins=Coins.from_proto(proto.token_out_mins)
        )


@attr.s
class MsgSwapExactAmountIn(Msg):
    """Swap an exact amount of tokens in for the amount of tokens out identified by denom via routes

    Args:
        sender: address of sender
        routes: routes to swap through
        token_in: token to swap in
        token_out_min_amount: minimum amount of token to swap out
    """

    type_amino = "wasm/SwapExactAmountIn"
    """"""
    type_url = "/osmosis.gamm.v1beta1.SwapExactAmountIn"
    """"""
    prototype = MsgSwapExactAmountIn_pb
    """"""

    sender: AccAddress = attr.ib()
    routes:SwapAmountInRoute = attr.ib()
    token_in: Coin = attr.ib(converter=Coin)
    token_out_min_amount: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "routes": self.routes.to_amino(),
                "token_in": self.token_in.to_amino(),
                "token_out_min_amount": self.token_out_min_amount,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgSwapExactAmountIn:
        return cls(
            sender=data["sender"],
            routes=SwapAmountInRoute.from_data(data["routes"]),
            token_in=Coin.from_data(data["token_in"]),
            token_out_min_amount=data["token_out_min_amount"],
        )

    def to_proto(self) -> MsgSwapExactAmountIn_pb:
        return MsgSwapExactAmountIn_pb(
            sender=self.sender,
            routes=self.routes.to_proto(),
            contract=self.contract,
            token_in=self.token_in.to_proto(),
            token_out_min_amount=self.token_out_min_amount,
        )

    @classmethod
    def from_proto(cls, proto: MsgSwapExactAmountIn_pb) -> MsgSwapExactAmountIn:
        return cls(
            sender=proto.sender,
            routes=SwapAmountInRoute.from_proto(proto.routes),
            token_in=Coin.from_proto(proto.token_in),
            token_out_min_amount=proto.token_out_min_amount,
        )


@attr.s
class MsgSwapExactAmountOut(Msg):
    """ Swap an exact amount of tokens out for the amount of tokens in identified by denom via routes

    Args:
        sender: address of sender
        routes: routes to swap through
        token_in_max_amount: maximum amount of token to swap in
        token_out: token to swap out
    """

    type_amino = "wasm/SwapExactAmountOut"
    """"""
    type_url = "/osmosis.gamm.v1beta1.Msg/SwapExactAmountOut"
    """"""
    prototype = MsgSwapExactAmountOut_pb
    """"""

    sender: AccAddress = attr.ib()
    routes:SwapAmountOutRoute = attr.ib()
    token_in_max_amount: str = attr.ib()
    token_out: Coin = attr.ib(converter=Coin)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "routes": self.routes.to_amino(),
                "token_in_max_amount": self.token_in_max_amount,
                "token_out": self.token_out.to_amino(),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgSwapExactAmountOut:
        return cls(
            sender=data["sender"],
            routes=SwapAmountInRoute.from_data(data["routes"]),
            token_in_max_amount=data["token_in_max_amount"],
            token_out=Coin.from_data(data["token_out"]),
        )

    def to_proto(self) -> MsgSwapExactAmountOut_pb:
        return MsgSwapExactAmountOut_pb(
            sender=self.sender,
            routes=self.routes.to_proto(),
            contract=self.contract,
            token_in_max_amount=self.token_in_max_amount,
            token_out=self.token_out.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: MsgSwapExactAmountOut_pb) -> MsgSwapExactAmountOut:
        return cls(
            sender=proto.sender,
            routes=SwapAmountInRoute.from_proto(proto.routes),
            token_in_max_amount=proto.token_in_max_amount,
            token_out=Coin.from_proto(proto.token_out),
        )


@attr.s
class MsgJoinSwapExternAmountIn(Msg):
    """ Swap an exact amounts of tokens in for pool shares

    Args:
        sender: address of sender
        pool_id: pool id
        token_in: token to swap in
        shares_out_min_amount: minimum amount of shares to swap out
    """

    type_amino = "osmosis/JoinSwapExternAmountIn"
    """"""
    type_url = "/osmosis.gamm.v1beta1.Msg/JoinSwapExternAmountIn"
    """"""
    prototype = MsgJoinSwapExternAmountIn_pb
    """"""

    sender: AccAddress = attr.ib()
    pool_id: int = attr.ib()
    token_in: Coin = attr.ib(converter=Coin)
    shares_out_min_amount: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "pool_id": self.pool_id,
                "token_in": self.token_in.to_amino(),
                "shares_out_min_amount": self.shares_out_min_amount,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgJoinSwapExternAmountIn:
        return cls(
            sender=data["sender"],
            pool_id=data["pool_id"],
            token_in=Coin.from_data(data["token_in"]),
            shares_out_min_amount=data["shares_out_min_amount"],
        )

    def to_proto(self) -> MsgJoinSwapExternAmountIn_pb:
        return MsgJoinSwapExternAmountIn_pb(
            sender=self.sender,
            pool_id=self.pool_id,
            token_in=self.token_in.to_proto(),
            shares_out_min_amount=self.shares_out_min_amount,
        )

    @classmethod
    def from_proto(cls, proto: MsgJoinSwapExternAmountIn_pb) -> MsgJoinSwapExternAmountIn:
        return cls(
            sender=proto.sender,
            pool_id=proto.pool_id,
            token_in=Coin.from_proto(proto.token_in),
            shares_out_min_amount=proto.shares_out_min_amount,
        )



@attr.s
class MsgJoinSwapShareAmountOut(Msg):
    """ 

    Args:
        sender: address of sender
        pool_id: pool id
        token_in_denoms: token to swap in
        share_out_amount: amount of shares to swap out
        token_in_max_amounts: maximum amount of tokens to swap in
    """

    type_amino = "osmosis/JoinSwapShareAmountOut"
    """"""
    type_url = "/osmosis.gamm.v1beta1.Msg/JoinSwapShareAmountOut"
    """"""
    prototype = MsgJoinSwapShareAmountOut_pb
    """"""

    sender: AccAddress = attr.ib()
    pool_id: int = attr.ib()
    token_in_denom: str = attr.ib()
    share_out_amount: str = attr.ib()
    token_in_max_amount: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "pool_id": self.pool_id,
                "token_in_denom": self.token_in_denom,
                "share_out_amount": self.share_out_amount,
                "token_in_max_amount": self.token_in_max_amount,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgJoinSwapShareAmountOut:
        return cls(
            sender=data["sender"],
            pool_id=data["pool_id"],
            token_in_denom=data["token_in_denom"],
            share_out_amount=data["share_out_amount"],
            token_in_max_amount=data["token_in_max_amount"],
        )

    def to_proto(self) -> MsgJoinSwapShareAmountOut_pb:
        return MsgJoinSwapShareAmountOut_pb(
            sender=self.sender,
            pool_id=self.pool_id,
            token_in_denom=self.token_in_denom,
            share_out_amount=self.share_out_amount,
            token_in_max_amount=self.token_in_max_amount,
        )

    @classmethod
    def from_proto(cls, proto: MsgJoinSwapShareAmountOut_pb) -> MsgJoinSwapShareAmountOut:
        return cls(
            sender=proto.sender,
            pool_id=proto.pool_id,
            token_in_denom=proto.token_in_denom,
            share_out_amount=proto.share_out_amount,
            token_in_max_amount=proto.token_in_max_amount,
        )



@attr.s
class MsgExitSwapShareAmountIn(Msg):
    """ 
    Args:
        sender: address of sender
        pool_id: pool id
        token_out_denom: token to swap in
        share_in_amount: amount of shares to swap out
        token_out_min_amount: maximum amount of tokens to swap in
    """

    type_amino = "osmosis/ExitSwapShareAmountIn"
    """"""
    type_url = "/osmosis.gamm.v1beta1.Msg/ExitSwapShareAmountIn"
    """"""
    prototype = MsgExitSwapShareAmountIn_pb
    """"""

    sender: AccAddress = attr.ib()
    pool_id: int = attr.ib()
    token_out_denom: str = attr.ib()
    share_in_amount: str = attr.ib()
    token_out_min_amount: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "pool_id": self.pool_id,
                "token_out_denom": self.token_out_denom,
                "share_in_amount": self.share_in_amount,
                "token_out_min_amount": self.token_out_min_amount,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgExitSwapShareAmountIn:
        return cls(
            sender=data["sender"],
            pool_id=data["pool_id"],
            token_out_denom=data["token_out_denom"],
            share_in_amount=data["share_in_amount"],
            token_out_min_amount=data["token_out_min_amount"],
        )

    def to_proto(self) -> MsgExitSwapShareAmountIn_pb:
        return MsgExitSwapShareAmountIn_pb(
            sender=self.sender,
            pool_id=self.pool_id,
            token_out_denom=self.token_out_denom,
            share_in_amount=self.share_in_amount,
            token_out_min_amount=self.token_out_min_amount,
        )

    @classmethod
    def from_proto(cls, proto: MsgExitSwapShareAmountIn_pb) -> MsgExitSwapShareAmountIn:
        return cls(
            sender=proto.sender,
            pool_id=proto.pool_id,
            token_out_denom=proto.token_out_denom,
            share_in_amount=proto.share_in_amount,
            token_out_min_amount=proto.token_out_min_amount,
        )



@attr.s
class MsgExitSwapExternAmountOut(Msg):
    """ 
    Args:
        sender: address of sender
        pool_id: pool id
        token_out: token to swap out
        share_in_amount: amount of shares to swap out
        share_in_max_amount: maximum amount of shares to swap in
    """

    type_amino = "osmosis/ExitSwapExternAmountOut"
    """"""
    type_url = "/osmosis.gamm.v1beta1.Msg/ExitSwapExternAmountOut"
    """"""
    prototype = MsgExitSwapExternAmountOut_pb
    """"""

    sender: AccAddress = attr.ib()
    pool_id: int = attr.ib()
    token_out: Coin = attr.ib()
    share_in_max_amount: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "pool_id": self.pool_id,
                "token_out": self.token_out.to_amino(),
                "share_in_max_amount": self.share_in_max_amount,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgExitSwapShareAmountIn:
        return cls(
            sender=data["sender"],
            pool_id=data["pool_id"],
            token_out_denom=data["token_out"],
            share_in_max_amount=data["share_in_max_amount"],
        )

    def to_proto(self) -> MsgExitSwapExternAmountOut:
        return MsgExitSwapExternAmountOut(
            sender=self.sender,
            pool_id=self.pool_id,
            token_out_denom=self.token_out,
            share_in_max_amount=self.share_in_max_amount,
        )

    @classmethod
    def from_proto(cls, proto: MsgExitSwapExternAmountOut) -> MsgExitSwapShareAmountIn:
        return cls(
            sender=proto.sender,
            pool_id=proto.pool_id,
            token_out=proto.token_out,
            share_in_max_amount=proto.share_in_max_amount,
        )








