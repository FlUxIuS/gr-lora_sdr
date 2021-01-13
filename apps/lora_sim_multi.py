#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Simulated multi stream
# Author: Martyn van Dijke
# GNU Radio version: 3.8.2.0

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import lora_sdr


class lora_sim_multi(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Simulated multi stream")

        ##################################################
        # Variables
        ##################################################
        self.bw = bw = 250000
        self.sf1 = sf1 = 7
        self.sf = sf = 11
        self.samp_rate = samp_rate = bw
        self.pay_len = pay_len = 64
        self.n_frame = n_frame = 10
        self.multi_control = multi_control = False
        self.mult_const = mult_const = 1
        self.impl_head = impl_head = True
        self.has_crc = has_crc = False
        self.frame_period = frame_period = 200
        self.cr = cr = 4

        ##################################################
        # Blocks
        ##################################################
        self.lora_sdr_multi_control_1 = lora_sdr.multi_control(2)
        self.lora_sdr_hier_tx_0_2 = lora_sdr.hier_tx(pay_len, n_frame, 'sTomvXMuARDzMfJltZ4xSJ0dLGMDueK8PH00maiTXhiew9HzJmZzKNoP4zHkWGRC', cr, sf1, impl_head,has_crc, samp_rate, bw, 200, True)
        self.lora_sdr_hier_tx_0 = lora_sdr.hier_tx(pay_len, n_frame, 'sTomvXMuARDzMfJltZ4xSJ0dLGMDueK8PH00maiTXhiew9HzJmZzKNoP4zHkWGRC', cr, sf, impl_head,has_crc, samp_rate, bw, 200, True)
        self.lora_sdr_hier_rx_0 = lora_sdr.hier_rx(samp_rate, bw, sf, impl_head, cr, pay_len, has_crc)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccf(4, (-0.128616616593872,-0.212206590789194,-0.180063263231421,3.89817183251938e-17,0.300105438719035,0.636619772367581,0.900316316157106,1,0.900316316157106,0.636619772367581,0.300105438719035,3.89817183251938e-17,-0.180063263231421,-0.212206590789194,-0.128616616593872))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.interp_fir_filter_xxx_0.set_min_output_buffer(16384)
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,False)
        self.blocks_message_debug_0_0 = blocks.message_debug()
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_add_xx_0 = blocks.add_vcc(1)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.lora_sdr_hier_rx_0, 'ctrl_out'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.lora_sdr_hier_rx_0, 'ctrl_out'), (self.lora_sdr_multi_control_1, 'ctrl_in'))
        self.msg_connect((self.lora_sdr_multi_control_1, 'ctrl_out0'), (self.blocks_message_debug_0_0, 'print'))
        self.msg_connect((self.lora_sdr_multi_control_1, 'ctrl_out1'), (self.lora_sdr_hier_tx_0, 'ctrl_in'))
        self.msg_connect((self.lora_sdr_multi_control_1, 'ctrl_out0'), (self.lora_sdr_hier_tx_0_2, 'ctrl_in'))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_throttle_1, 0))
        self.connect((self.blocks_throttle_1, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.lora_sdr_hier_rx_0, 0))
        self.connect((self.lora_sdr_hier_tx_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.lora_sdr_hier_tx_0_2, 0), (self.blocks_add_xx_0, 0))


    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.set_samp_rate(self.bw)

    def get_sf1(self):
        return self.sf1

    def set_sf1(self, sf1):
        self.sf1 = sf1

    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_1.set_sample_rate(self.samp_rate)

    def get_pay_len(self):
        return self.pay_len

    def set_pay_len(self, pay_len):
        self.pay_len = pay_len

    def get_n_frame(self):
        return self.n_frame

    def set_n_frame(self, n_frame):
        self.n_frame = n_frame

    def get_multi_control(self):
        return self.multi_control

    def set_multi_control(self, multi_control):
        self.multi_control = multi_control

    def get_mult_const(self):
        return self.mult_const

    def set_mult_const(self, mult_const):
        self.mult_const = mult_const

    def get_impl_head(self):
        return self.impl_head

    def set_impl_head(self, impl_head):
        self.impl_head = impl_head

    def get_has_crc(self):
        return self.has_crc

    def set_has_crc(self, has_crc):
        self.has_crc = has_crc

    def get_frame_period(self):
        return self.frame_period

    def set_frame_period(self, frame_period):
        self.frame_period = frame_period

    def get_cr(self):
        return self.cr

    def set_cr(self, cr):
        self.cr = cr





def main(top_block_cls=lora_sim_multi, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
