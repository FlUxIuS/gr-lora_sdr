#include "fft_demod_impl.h"
#include <gnuradio/io_signature.h>
//Fix for libboost > 1.75
#include <boost/bind/placeholders.hpp>

using namespace boost::placeholders;

extern "C" {
#include "kiss_fft.h"
}

namespace gr {
namespace lora_sdr {

fft_demod::sptr fft_demod::make(float samp_rate, uint32_t bandwidth, uint8_t sf,
                                bool impl_head) {
  return gnuradio::get_initial_sptr(
      new fft_demod_impl(samp_rate, bandwidth, sf, impl_head));
}

/**
 * @brief Construct a new fft demod impl object
 *
 * @param samp_rate : sampling rate
 * @param bandwidth : bandwith
 * @param sf : spreading factor
 * @param impl_head : impl_head mode
 */
fft_demod_impl::fft_demod_impl(float samp_rate, uint32_t bandwidth, uint8_t sf,
                               bool impl_head)
    : gr::block("fft_demod",
                gr::io_signature::make(1, 1, (1u << sf) * sizeof(gr_complex)),
                gr::io_signature::make(0, 1, sizeof(uint32_t))) {
  m_bw = bandwidth;
  m_samp_rate = samp_rate;
  m_sf = sf;

  m_number_of_bins = (uint32_t)(1u << m_sf);
  m_samples_per_symbol = (uint32_t)(m_samp_rate * m_number_of_bins / m_bw);
  is_first = true;
  m_upchirp.resize(m_samples_per_symbol);
  m_downchirp.resize(m_samples_per_symbol);

  // FFT demodulation preparations
  m_fft.resize(m_samples_per_symbol);
  m_dechirped.resize(m_samples_per_symbol);

  // register message ports
  message_port_register_in(pmt::mp("new_frame"));
  set_msg_handler(pmt::mp("new_frame"),
                  boost::bind(&fft_demod_impl::new_frame_handler, this, _1));

  message_port_register_in(pmt::mp("CR"));
  set_msg_handler(pmt::mp("CR"),
                  boost::bind(&fft_demod_impl::header_cr_handler, this, _1));
  set_thread_priority(98);
  set_tag_propagation_policy(TPP_ALL_TO_ALL);
  // #ifdef GRLORA_DEBUG
  // // idx_file.open("../matlab/stats/idx.txt", std::ios::out | std::ios::trunc
  // ); #endif
}

/**
 * @brief Destroy the fft demod impl object
 *
 */
fft_demod_impl::~fft_demod_impl() {}

/**
 * @brief Standard gnuradio function to tell the system how many input and
 * output items are needed.
 *
 * @param noutput_items : number of output items
 * @param ninput_items_required : number of output items required
 */
void fft_demod_impl::forecast(int noutput_items,
                              gr_vector_int &ninput_items_required) {
  ninput_items_required[0] = 1;
}

int32_t fft_demod_impl::get_symbol_val(const gr_complex *samples) {
  float m_fft_mag[m_number_of_bins];
  float rec_en = 0;
  kiss_fft_cfg cfg = kiss_fft_alloc(m_samples_per_symbol, 0, 0, 0);
  kiss_fft_cpx *cx_in = new kiss_fft_cpx[m_samples_per_symbol];
  kiss_fft_cpx *cx_out = new kiss_fft_cpx[m_samples_per_symbol];

  // Multiply with ideal downchirp
  volk_32fc_x2_multiply_32fc(&m_dechirped[0], samples, &m_downchirp[0],
                             m_samples_per_symbol);
  for (int i = 0; i < m_samples_per_symbol; i++) {
    cx_in[i].r = m_dechirped[i].real();
    cx_in[i].i = m_dechirped[i].imag();
  }
  // do the FFT
  kiss_fft(cfg, cx_in, cx_out);
  // Get magnitude
  for (uint32_t i = 0u; i < m_number_of_bins; i++) {
    m_fft_mag[i] = cx_out[i].r * cx_out[i].r + cx_out[i].i * cx_out[i].i;
    rec_en += m_fft_mag[i];
  }

  free(cfg);
  delete[] cx_in;
  delete[] cx_out;
  // Return argmax

  int idx =
      std::max_element(m_fft_mag, m_fft_mag + m_number_of_bins) - m_fft_mag;
  // #ifdef GRLORA_DEBUG
  //   // idx_file<<idx<<", ";
  // #endif
  return (idx);
}

void fft_demod_impl::new_frame_handler(pmt::pmt_t id) {
  is_first = true;
  received_cr = false;
#ifdef GRLORA_MEASUREMENTS
  energy_file << "\n";
#endif
  // create downchirp taking CFOint into account
  build_upchirp(&m_upchirp[0], pmt::to_long(id), m_sf);
  volk_32fc_conjugate_32fc(&m_downchirp[0], &m_upchirp[0], m_number_of_bins);
  output.clear();
};

void fft_demod_impl::header_cr_handler(pmt::pmt_t cr) {
  m_cr = pmt::to_long(cr);
  received_cr = true;
};

/**
 * @brief Main function where the actual computation is done
 *
 * @param noutput_items : number of output items to produce
 * @param ninput_items : number of input items
 * @param input_items : input item (i.e. output of the frame sync stage)
 * @param output_items : output data
 * @return int
 */
int fft_demod_impl::general_work(int noutput_items, gr_vector_int &ninput_items,
                                 gr_vector_const_void_star &input_items,
                                 gr_vector_void_star &output_items) {
  const gr_complex *in = (const gr_complex *)input_items[0];
  uint32_t *out = (uint32_t *)output_items[0];

  if (is_first || received_cr) {
    // shift by -1 and use reduce rate if first block (header)
    output.push_back(mod(get_symbol_val(in) - 1, (1 << m_sf)) /
                     (is_first ? 4 : 1));
    block_size = 4 + (is_first ? 4 : m_cr);
    if ((output.size() == block_size)) {
      is_first = false;
      memcpy(&out[0], &output[0], block_size * sizeof(uint32_t));

      output.clear();
      noutput_items = block_size;
    } else
      noutput_items = 0;
    consume_each(1);
    return noutput_items;
  }
  return 0;
}

} /* namespace lora_sdr */
} /* namespace gr */
