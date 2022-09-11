from __future__ import annotations

import json
from typing import List, Optional, Union

import attr
from osmosis_protobuf.osmosis.gamm import SwapAmountInRoute as SwapAmountInRoute_pb
from osmosis_protobuf.osmosis.gamm import SwapAmountOutRoute as SwapAmountOutRoute_pb

from cosmos_sdk.core.bech32 import AccAddress
from cosmos_sdk.core.msg import Msg
from cosmos_sdk.util.json import JSONSerializable

__all__ = ["SwapAmountInRoute", "SwapAmountOutRoute"]

@attr.s
class SwapAmountInRoute(JSONSerializable):

    pool_id = attr.ib()
    token_out_denom: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "pool_id": self.pool_id,
            "token_out_denom": self.token_out_denom,
        }

    def to_data(self) -> dict:
        return {
            "pool_id": self.pool_id,
            "token_out_denom": self.token_out_denom,
        }

    def to_proto(self) -> SwapAmountInRoute_pb:
        return SwapAmountInRoute_pb(pool_id=self.pool_id, token_out_denom=self.token_out_denom)

    @classmethod
    def from_data(cls, data: dict) -> SwapAmountInRoute:
        return cls(
            pool_id= data["pool_id"],
            token_out_denom=data["token_out_denom"],
        )

    @classmethod
    def from_proto(cls, proto: SwapAmountInRoute_pb) -> SwapAmountInRoute:
        return cls(pool_id=proto.pool_id, token_out_denom=proto.token_out_denom)

@attr.s
class SwapAmountOutRoute(JSONSerializable):

    pool_id = attr.ib()
    token_in_denom: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "pool_id": self.pool_id,
            "token_in_denom": self.token_in_denom,
        }

    def to_data(self) -> dict:
        return {
            "pool_id": self.pool_id,
            "token_in_denom": self.token_in_denom,
        }

    def to_proto(self) -> SwapAmountOutRoute_pb:
        return SwapAmountOutRoute_pb(pool_id=self.pool_id, token_in_denom=self.token_in_denom)

    @classmethod
    def from_data(cls, data: dict) -> SwapAmountOutRoute:
        return cls(
            pool_id= data["pool_id"],
            token_in_denom=data["token_in_denom"],
        )

    @classmethod
    def from_proto(cls, proto: SwapAmountOutRoute_pb) -> SwapAmountOutRoute:
        return cls(pool_id=proto.pool_id, token_in_denom=proto.token_in_denom)
