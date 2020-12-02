    def test_@@filename@@(self):
        ##################################################
        # Variables
        ##################################################
        #input data into the system
        src_data = "@@source_data@@"
        self.bw = bw = 250000
        self.sf = sf = 5
        self.samp_rate = samp_rate = 250000
        self.pay_len = pay_len = 64
        self.n_frame = n_frame = 1
        self.impl_head = impl_head = True
        self.has_crc = has_crc = True
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
        self.blocks_message_debug_0 = blocks.message_debug()

        #get the writen file
        base = os.getcwd()
        file_result = base+"/../../test_files/@@filename@@_result.txt"
        f = open(file_result, "r")
        vector = f.read()
        f.close()
        #transform vector string from file to the right format
        vector = ast.literal_eval(vector)
        self.blocks_vector_source_x_0 = blocks.vector_source_c(vector, False, 1, [])


        ##################################################
        # Connections
        ##################################################
        self.tb.msg_connect((self.lora_sdr_crc_verif_0, 'msg'), (self.blocks_message_debug_0, 'store'))
        self.tb.msg_connect((self.lora_sdr_frame_sync_0, 'new_frame'), (self.lora_sdr_deinterleaver_0, 'new_frame'))
        self.tb.msg_connect((self.lora_sdr_frame_sync_0, 'new_frame'), (self.lora_sdr_dewhitening_0, 'new_frame'))
        self.tb.msg_connect((self.lora_sdr_frame_sync_0, 'new_frame'), (self.lora_sdr_fft_demod_0, 'new_frame'))
        self.tb.msg_connect((self.lora_sdr_frame_sync_0, 'new_frame'), (self.lora_sdr_hamming_dec_0, 'new_frame'))
        self.tb.msg_connect((self.lora_sdr_frame_sync_0, 'new_frame'), (self.lora_sdr_header_decoder_0, 'new_frame'))
        self.tb.msg_connect((self.lora_sdr_header_decoder_0, 'pay_len'), (self.lora_sdr_crc_verif_0, 'pay_len'))
        self.tb.msg_connect((self.lora_sdr_header_decoder_0, 'CRC'), (self.lora_sdr_crc_verif_0, 'CRC'))
        self.tb.msg_connect((self.lora_sdr_header_decoder_0, 'CR'), (self.lora_sdr_deinterleaver_0, 'CR'))
        self.tb.msg_connect((self.lora_sdr_header_decoder_0, 'pay_len'), (self.lora_sdr_dewhitening_0, 'pay_len'))
        self.tb.msg_connect((self.lora_sdr_header_decoder_0, 'CRC'), (self.lora_sdr_dewhitening_0, 'CRC'))
        self.tb.msg_connect((self.lora_sdr_header_decoder_0, 'CR'), (self.lora_sdr_fft_demod_0, 'CR'))
        self.tb.msg_connect((self.lora_sdr_header_decoder_0, 'CR'), (self.lora_sdr_frame_sync_0, 'CR'))
        self.tb.msg_connect((self.lora_sdr_header_decoder_0, 'err'), (self.lora_sdr_frame_sync_0, 'err'))
        self.tb.msg_connect((self.lora_sdr_header_decoder_0, 'CRC'), (self.lora_sdr_frame_sync_0, 'crc'))
        self.tb.msg_connect((self.lora_sdr_header_decoder_0, 'pay_len'), (self.lora_sdr_frame_sync_0, 'pay_len'))
        self.tb.msg_connect((self.lora_sdr_header_decoder_0, 'CR'), (self.lora_sdr_hamming_dec_0, 'CR'))
        self.tb.connect((self.lora_sdr_deinterleaver_0, 0), (self.lora_sdr_hamming_dec_0, 0))
        self.tb.connect((self.lora_sdr_dewhitening_0, 0), (self.lora_sdr_crc_verif_0, 0))
        self.tb.connect((self.lora_sdr_fft_demod_0, 0), (self.lora_sdr_gray_enc_0, 0))
        self.tb.connect((self.lora_sdr_frame_sync_0, 0), (self.lora_sdr_fft_demod_0, 0))
        self.tb.connect((self.lora_sdr_gray_enc_0, 0), (self.lora_sdr_deinterleaver_0, 0))
        self.tb.connect((self.lora_sdr_hamming_dec_0, 0), (self.lora_sdr_header_decoder_0, 0))
        self.tb.connect((self.lora_sdr_header_decoder_0, 0), (self.lora_sdr_dewhitening_0, 0))
        self.tb.connect((self.rational_resampler_xxx_0, 0), (self.lora_sdr_frame_sync_0, 0))
        self.tb.connect((self.blocks_vector_source_x_0, 0), (self.rational_resampler_xxx_0, 0))
        

        #run the flowgraph
        self.tb.run()
        #get the message from the store port of the message debug printer
        msg = self.blocks_message_debug_0.get_message(0)

        # #self.tb.run()
        # self.tb.start()
        # time.sleep(10)
        # self.tb.stop()
        # self.tb.wait()
        self.assertMultiLineEqual(src_data,msg,msg="Error decoded data is not the same as input data")