#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.8.1.0

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


class test_tx(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet")

        ##################################################
        # Variables
        ##################################################
        self.bw = bw = 250000
        self.sf = sf = 7
        self.samp_rate = samp_rate = bw
        self.pay_len = pay_len = 5
        self.n_frame = n_frame = 2
        self.mult_const = mult_const = 1
        self.impl_head = impl_head = True
        self.has_crc = has_crc = False
        self.frame_period = frame_period = 200
        self.cr = cr = 0

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=4,
                decimation=1,
                taps=None,
                fractional_bw=None)
        self.lora_sdr_header_decoder_0 = lora_sdr.header_decoder(impl_head, cr, pay_len, has_crc)
        self.lora_sdr_hamming_dec_0 = lora_sdr.hamming_dec()
        self.lora_sdr_gray_enc_0 = lora_sdr.gray_enc()
        self.lora_sdr_frame_sync_0 = lora_sdr.frame_sync(samp_rate, bw, sf, impl_head)
        self.lora_sdr_fft_demod_0 = lora_sdr.fft_demod(samp_rate, bw, sf, impl_head)
        self.lora_sdr_dewhitening_0 = lora_sdr.dewhitening()
        self.lora_sdr_deinterleaver_0 = lora_sdr.deinterleaver(sf)
        self.lora_sdr_crc_verif_0 = lora_sdr.crc_verif()
        self.blocks_vector_source_x_0 = blocks.vector_source_c(((0.8999999761581421+0j), (-0.895666241645813-0.08821538090705872j), (0.8314915895462036+0.3444150686264038j), (-0.5709542036056519-0.6957091689109802j), (-2.610600233765581e-07+0.8999999761581421j), (0.6957091689109802-0.5709542036056519j), (-0.8314914107322693-0.34441545605659485j), (-0.08821620047092438+0.8956661820411682j), (0.8999999761581421-4.2929567456440054e-08j), (0.08821505308151245-0.8956663012504578j), (-0.8314916491508484-0.34441491961479187j)), True, 1, [])
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex*1, 2)
        self.blocks_message_debug_0 = blocks.message_debug()



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.lora_sdr_crc_verif_0, 'msg'), (self.blocks_message_debug_0, 'store'))
        self.msg_connect((self.lora_sdr_frame_sync_0, 'new_frame'), (self.lora_sdr_deinterleaver_0, 'new_frame'))
        self.msg_connect((self.lora_sdr_frame_sync_0, 'new_frame'), (self.lora_sdr_dewhitening_0, 'new_frame'))
        self.msg_connect((self.lora_sdr_frame_sync_0, 'new_frame'), (self.lora_sdr_fft_demod_0, 'new_frame'))
        self.msg_connect((self.lora_sdr_frame_sync_0, 'new_frame'), (self.lora_sdr_hamming_dec_0, 'new_frame'))
        self.msg_connect((self.lora_sdr_frame_sync_0, 'new_frame'), (self.lora_sdr_header_decoder_0, 'new_frame'))
        self.msg_connect((self.lora_sdr_header_decoder_0, 'CRC'), (self.lora_sdr_crc_verif_0, 'CRC'))
        self.msg_connect((self.lora_sdr_header_decoder_0, 'pay_len'), (self.lora_sdr_crc_verif_0, 'pay_len'))
        self.msg_connect((self.lora_sdr_header_decoder_0, 'CR'), (self.lora_sdr_deinterleaver_0, 'CR'))
        self.msg_connect((self.lora_sdr_header_decoder_0, 'CRC'), (self.lora_sdr_dewhitening_0, 'CRC'))
        self.msg_connect((self.lora_sdr_header_decoder_0, 'pay_len'), (self.lora_sdr_dewhitening_0, 'pay_len'))
        self.msg_connect((self.lora_sdr_header_decoder_0, 'CR'), (self.lora_sdr_fft_demod_0, 'CR'))
        self.msg_connect((self.lora_sdr_header_decoder_0, 'err'), (self.lora_sdr_frame_sync_0, 'err'))
        self.msg_connect((self.lora_sdr_header_decoder_0, 'CRC'), (self.lora_sdr_frame_sync_0, 'crc'))
        self.msg_connect((self.lora_sdr_header_decoder_0, 'pay_len'), (self.lora_sdr_frame_sync_0, 'pay_len'))
        self.msg_connect((self.lora_sdr_header_decoder_0, 'CR'), (self.lora_sdr_frame_sync_0, 'CR'))
        self.msg_connect((self.lora_sdr_header_decoder_0, 'CR'), (self.lora_sdr_hamming_dec_0, 'CR'))
        self.connect((self.blocks_repeat_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.lora_sdr_deinterleaver_0, 0), (self.lora_sdr_hamming_dec_0, 0))
        self.connect((self.lora_sdr_dewhitening_0, 0), (self.lora_sdr_crc_verif_0, 0))
        self.connect((self.lora_sdr_fft_demod_0, 0), (self.lora_sdr_gray_enc_0, 0))
        self.connect((self.lora_sdr_frame_sync_0, 0), (self.lora_sdr_fft_demod_0, 0))
        self.connect((self.lora_sdr_gray_enc_0, 0), (self.lora_sdr_deinterleaver_0, 0))
        self.connect((self.lora_sdr_hamming_dec_0, 0), (self.lora_sdr_header_decoder_0, 0))
        self.connect((self.lora_sdr_header_decoder_0, 0), (self.lora_sdr_dewhitening_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.lora_sdr_frame_sync_0, 0))


    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.set_samp_rate(self.bw)

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





def main(top_block_cls=test_tx, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
