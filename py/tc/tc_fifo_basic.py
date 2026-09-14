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
# tc_fifo_basic
#
# Fills the FIFO to exactly full, then drains it to exactly empty.
#
# Writes 8 values into a depth-8 FIFO, asserting on each that ing_full is
# still low beforehand -- so the FIFO is proven to accept every one of them
# rather than silently dropping the last. After the eighth, ing_full must be
# high and sr_fill_level must read 8: the boundary is checked from both
# sides, since a FIFO that fills one short or one late passes a simple
# write-then-read test.
#
# Reads then check the values come back in the order they went in.
#
################################################################################

from __future__ import annotations

from cocotb.triggers import FallingEdge, ReadOnly, RisingEdge, Timer

from fifo_base_test import fifo_base_test


class tc_fifo_basic(fifo_base_test):

  async def run_phase(self):
    self.raise_objection()
    vif = self.vif
    scoreboard = self.env.scoreboard0

    vif.rst_n.value = 0
    vif.ing_enable.value = 0
    vif.egr_enable.value = 0
    vif.ing_data.value = 0
    vif.cr_almost_full_level.value = 7
    for _ in range(3):
      await RisingEdge(vif.clk)
    vif.rst_n.value = 1
    await Timer(1, unit="step")

    for value in range(8):
      await FallingEdge(vif.clk)
      vif.ing_data.value = value
      vif.ing_enable.value = 1
      vif.egr_enable.value = 0
      if int(vif.ing_full.value) != 0:
        raise AssertionError(f"FIFO became full before write {value}")
      scoreboard.write_accepted(value)
      await RisingEdge(vif.clk)
      await ReadOnly()
      await Timer(1, unit="step")

    assert int(vif.ing_full.value) == 1
    assert int(vif.sr_fill_level.value) == 8

    for expected in range(8):
      await FallingEdge(vif.clk)
      vif.ing_enable.value = 0
      vif.egr_enable.value = 1
      await ReadOnly()
      actual = int(vif.egr_data.value)
      await RisingEdge(vif.clk)
      scoreboard.read_accepted(actual)
      await Timer(1, unit="step")

    assert int(vif.egr_empty.value) == 1
    assert scoreboard.number_of_failed == 0
    self.drop_objection()
