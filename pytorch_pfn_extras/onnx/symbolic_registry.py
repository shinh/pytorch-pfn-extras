import pytorch_pfn_extras
from typing import Callable

if pytorch_pfn_extras.requires("1.13.0"):
    import torch.onnx._internal.registration as reg
    import torch.onnx.utils

    def is_registered_op(op_type: str, domain: str, opset_version: int) -> bool:
        return reg.registry.is_registered_op(f"{domain}::{op_type}", opset_version)

    def get_registered_op(op_type: str, domain: str, opset_version: int) -> Callable:
        group = reg.registry.get_function_group(f"{domain}::{op_type}")
        assert group is not None
        ret = group.get(opset_version)
        assert ret is not None
        return ret

    def register_op(op_type: str, f: Callable, domain: str, opset_version: int) -> None:
        if len(domain) == 0:
            domain = "aten"
        torch.onnx.utils.register_custom_op_symbolic(
            f"{domain}::{op_type}", f, opset_version)
else:
    from torch.onnx.symolic_registry import *
