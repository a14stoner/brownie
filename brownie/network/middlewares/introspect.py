from typing import Callable, Dict, List, Optional

from web3 import Web3

from brownie.network.middlewares import BrownieMiddlewareABC


class IntrospectionMiddleware(BrownieMiddlewareABC):

    """
    Middleware for introspection of raw RPC calls. Useful for debugging.

    Accessible via `web3._introspect`
    """

    def __init__(self, w3: Web3) -> None:
        w3._introspect = self
        self.reset_introspection()

    @classmethod
    def get_layer(cls, w3: Web3, network_type: str) -> Optional[int]:
        return 0

    def process_request(self, make_request: Callable, method: str, params: List) -> Dict:
        if self._is_enabled is not False and self._per_method_enabled.get(method) is not False:
            if self._per_method_raises.get(method):
                raise Exception(f"Encountered method: {method}")
            if self._is_enabled is True or self._per_method_enabled.get(method):
                print(f"{method}: {', '.join(str(i) for i in params)}")
        return make_request(method, params)

    def set_introspection(self, is_enabled: bool):
        self._is_enabled = is_enabled

    def set_method_introspection(self, method: str, is_enabled: bool, raises_exc: bool = None):
        self._per_method_enabled[method] = is_enabled
        if raises_exc is not None:
            self._per_method_raises[method] = raises_exc

    def reset_introspection(self):
        self._is_enabled = None
        self._per_method_enabled = {"eth_getFilterChanges": False}
        self._per_method_raises = {}
