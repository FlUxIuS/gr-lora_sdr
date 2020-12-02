    def test_@@filename@@(self):
        ##################################################
        # Variables
        ##################################################
        #input data into the system
        src_data = "@@source_data@@"
        self.bw = bw = @@bw@@
        self.sf = sf = @@sf@@
        self.samp_rate = samp_rate = @@bw@@
        self.pay_len = pay_len = @@pay_len@@
        self.n_frame = n_frame = 1
        self.impl_head = impl_head = @@impl_head@@
        self.has_crc = has_crc = @@has_crc@@
        self.frame_period = frame_period = 200
        self.cr = cr = @@cr@@

        ##################################################
        # Blocks
        ##################################################
        self.lora_sdr_whitening_0 = lora_sdr.whitening()
        self.lora_sdr_modulate_0 = lora_sdr.modulate(sf, samp_rate, bw)
        self.lora_sdr_modulate_0.set_min_output_buffer(10000000)
        self.lora_sdr_interleaver_0 = lora_sdr.interleaver(cr, sf)
        self.lora_sdr_header_0 = lora_sdr.header(impl_head, has_crc, cr)
        self.lora_sdr_hamming_enc_0 = lora_sdr.hamming_enc(cr, sf)
        self.lora_sdr_gray_decode_0 = lora_sdr.gray_decode(sf)
        self.lora_sdr_data_source_0_1_0 = lora_sdr.data_source(pay_len, n_frame, src_data)
        self.lora_sdr_add_crc_0 = lora_sdr.add_crc(has_crc)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_message_strobe_random_0_1_0 = blocks.message_strobe_random(pmt.intern(''), blocks.STROBE_UNIFORM, frame_period, 5)
        dst = blocks.vector_sink_c()


        ##################################################
        # Connections
        ##################################################
        self.tb.msg_connect((self.blocks_message_strobe_random_0_1_0, 'strobe'), (self.lora_sdr_data_source_0_1_0, 'trigg'))
        self.tb.msg_connect((self.lora_sdr_data_source_0_1_0, 'msg'), (self.lora_sdr_add_crc_0, 'msg'))
        self.tb.msg_connect((self.lora_sdr_data_source_0_1_0, 'msg'), (self.lora_sdr_header_0, 'msg'))
        self.tb.msg_connect((self.lora_sdr_data_source_0_1_0, 'msg'), (self.lora_sdr_interleaver_0, 'msg'))
        self.tb.msg_connect((self.lora_sdr_data_source_0_1_0, 'msg'), (self.lora_sdr_modulate_0, 'msg'))
        self.tb.msg_connect((self.lora_sdr_data_source_0_1_0, 'msg'), (self.lora_sdr_whitening_0, 'msg'))
        self.tb.connect((self.lora_sdr_add_crc_0, 0), (self.lora_sdr_hamming_enc_0, 0))
        self.tb.connect((self.lora_sdr_gray_decode_0, 0), (self.lora_sdr_modulate_0, 0))
        self.tb.connect((self.lora_sdr_hamming_enc_0, 0), (self.lora_sdr_interleaver_0, 0))
        self.tb.connect((self.lora_sdr_header_0, 0), (self.lora_sdr_add_crc_0, 0))
        self.tb.connect((self.lora_sdr_interleaver_0, 0), (self.lora_sdr_gray_decode_0, 0))
        self.tb.connect((self.lora_sdr_whitening_0, 0), (self.lora_sdr_header_0, 0))
        #connect to complex vector sink 
        self.tb.connect((self.lora_sdr_modulate_0, 0),dst) 

        #self.tb.run()
        self.tb.start()
        time.sleep(10)
        self.tb.stop()
        self.tb.wait()

        #get current working folder
        base = os.getcwd()
        #file with output data that is expected
        file_expected = base+"/../../test_files/@@filename@@_result.txt"

        #set the written data file
        file_result = base+"/../../test_files/tx_@@filename@@_result.txt"
        result_data = dst.data()
        f = open(file_result, "w")
        f.write(str(result_data))
        f.close()
        
        #compare the actual files
        self.assertTrue(filecmp.cmp(file_expected,file_result), 'Error test failed, expected data and actual data are not the same')