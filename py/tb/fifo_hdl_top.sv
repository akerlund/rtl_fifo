////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2026 Fredrik Åkerlund
// https://github.com/akerlund/rtl_fifo
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
//
// Description:
// HDL shell for the synchronous FIFO pyUVM testbench.
//
////////////////////////////////////////////////////////////////////////////////

`default_nettype none

module fifo_hdl_top #(
    parameter int DATA_WIDTH = 32,
    parameter int ADDR_WIDTH = 3,
    parameter int MAX_REG_BYTES = 256
  )(
    input wire clk,
    input wire rst_n,
    input wire ing_enable,
    input wire [DATA_WIDTH-1 : 0] ing_data,
    output wire ing_full,
    output wire ing_almost_full,
    input wire egr_enable,
    output wire [DATA_WIDTH-1 : 0] egr_data,
    output wire egr_empty,
    output wire [ADDR_WIDTH : 0] sr_fill_level,
    output wire [ADDR_WIDTH : 0] sr_max_fill_level,
    input wire [ADDR_WIDTH : 0] cr_almost_full_level
  );

  fifo #(
    .DATA_WIDTH_P    ( DATA_WIDTH    ),
    .ADDR_WIDTH_P    ( ADDR_WIDTH    ),
    .MAX_REG_BYTES_P ( MAX_REG_BYTES )
  ) fifo_i0 (
    .clk                ( clk                ),
    .rst_n              ( rst_n              ),
    .ing_enable        ( ing_enable        ),
    .ing_data          ( ing_data          ),
    .ing_full          ( ing_full          ),
    .ing_almost_full   ( ing_almost_full   ),
    .egr_enable        ( egr_enable        ),
    .egr_data          ( egr_data          ),
    .egr_empty         ( egr_empty         ),
    .sr_fill_level     ( sr_fill_level     ),
    .sr_max_fill_level ( sr_max_fill_level ),
    .cr_almost_full_level ( cr_almost_full_level )
  );

endmodule

`default_nettype wire
