################################################################################
#
# Copyright (C) 2026 Fredrik Åkerlund
# https://github.com/akerlund/rtl_fifo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Description:
# cocotb testbench top for the synchronous FIFO pyUVM port.
#
################################################################################

from __future__ import annotations

import os
import sys

import cocotb
from cocotb.clock import Clock
from pyuvm import ConfigDB, uvm_root

_HERE = os.path.dirname(os.path.abspath(__file__))
_PY_ROOT = os.path.dirname(_HERE)


for path in (_HERE, os.path.join(_PY_ROOT, "tc")):
  if not os.path.isdir(path):
    raise RuntimeError(f"fifo_tb_top: source directory not found: {path}")
  if path not in sys.path:
    sys.path.insert(0, path)

from tc_fifo_basic import tc_fifo_basic # noqa: E402,F401


async def _run(dut, test_name):
  cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
  ConfigDB().set(None, "*", "vif", dut)
  await uvm_root().run_test(test_name, keep_set={ConfigDB})


@cocotb.test(name="tc_fifo_basic", timeout_time=20, timeout_unit="ms")
async def tc_fifo_basic_test(dut):
  await _run(dut, "tc_fifo_basic")
