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
# pyUVM scoreboard for the synchronous FIFO.
#
################################################################################

from __future__ import annotations

from pyuvm import uvm_component


class fifo_scoreboard(uvm_component):

  def __init__(self, name, parent):
    super().__init__(name, parent)
    self.expected = []
    self.number_of_writes = 0
    self.number_of_reads = 0
    self.number_of_failed = 0

  def write_accepted(self, data):
    self.expected.append(int(data))
    self.number_of_writes += 1

  def read_accepted(self, data):
    self.number_of_reads += 1
    if not self.expected:
      self.number_of_failed += 1
      self.logger.error(f"Unexpected FIFO read data={int(data)}")
      return
    expected = self.expected.pop(0)
    if int(data) != expected:
      self.number_of_failed += 1
      self.logger.error(
        f"FIFO mismatch: expected={expected} actual={int(data)}")

  def check_phase(self):
    if self.expected:
      self.number_of_failed += len(self.expected)
      self.logger.error(f"FIFO has {len(self.expected)} unread expected values")
    if self.number_of_failed:
      self.logger.error(f"FIFO test failed ({self.number_of_failed} errors)")
    else:
      self.logger.info(
        f"FIFO test passed ({self.number_of_writes} writes, "
        f"{self.number_of_reads} reads)")
