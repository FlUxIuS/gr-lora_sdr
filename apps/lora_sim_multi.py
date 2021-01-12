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
from gnuradio import gr
from gnuradio.filter import firdes
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
        self.sf6 = sf6 = 12
        self.sf5 = sf5 = 11
        self.sf4 = sf4 = 10
        self.sf3 = sf3 = 9
        self.sf2 = sf2 = 8
        self.sf = sf = 12
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
        self.lora_sdr_hier_tx_0 = lora_sdr.hier_tx(pay_len, n_frame, 'sTomvXMuARDzMfJltZ4xSJ0dLGMDueK8PH00maiTXhiew9HzJmZzKNoP4zHkWGRC', cr, sf, impl_head,has_crc, samp_rate, bw, 200, multi_control)
        self.blocks_tag_debug_0_1 = blocks.tag_debug(gr.sizeof_gr_complex*1, 'after_tx', "")
        self.blocks_tag_debug_0_1.set_display(True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.lora_sdr_hier_tx_0, 0), (self.blocks_tag_debug_0_1, 0))


    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.set_samp_rate(self.bw)

    def get_sf6(self):
        return self.sf6

    def set_sf6(self, sf6):
        self.sf6 = sf6

    def get_sf5(self):
        return self.sf5

    def set_sf5(self, sf5):
        self.sf5 = sf5

    def get_sf4(self):
        return self.sf4

    def set_sf4(self, sf4):
        self.sf4 = sf4

    def get_sf3(self):
        return self.sf3

    def set_sf3(self, sf3):
        self.sf3 = sf3

    def get_sf2(self):
        return self.sf2

    def set_sf2(self, sf2):
        self.sf2 = sf2

    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

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
