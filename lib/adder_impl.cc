/**
 * @file adder_impl.cc
 * @author Martyn van Dijke (martijnvdijke600@gmail.com)
 * @brief
 * @version 0.1
 * @date 2021-01-12
 *
 *
 */
#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "adder_impl.h"
#include <gnuradio/io_signature.h>
#include <volk/volk.h>

namespace gr {
namespace lora_sdr {

adder::sptr adder::make() {
  return gnuradio::get_initial_sptr(new adder_impl());
}

/**
 * @brief Construct a new adder impl::adder impl object
 *
 */
adder_impl::adder_impl()
    : gr::sync_block("adder", gr::io_signature::make(1, 10, sizeof(gr_complex)),
                     gr::io_signature::make(1, 1, sizeof(gr_complex))) {}

/**
 * @brief Destroy the adder impl::adder impl object
 *
 */
adder_impl::~adder_impl() { set_tag_propagation_policy(TPP_ALL_TO_ALL); }

int adder_impl::work(int noutput_items, gr_vector_const_void_star &input_items,
                     gr_vector_void_star &output_items) {
  // get number of input ports
  // int ninputs = input_items.size();

  // gr_complex *out = (gr_complex *)output_items[0];
  // int val = (gr_complex *) input_items[0](0);
  // std::cout << val << std::endl;
  // int test = ((gr_complex *)input_items[0])->imag();
  // std::cout << test << std::endl;
  // // int test = ((gr_complex *)input_items[0])->real()[0];
  // // int test = ((gr_complex *)input_items[0])->real();
  // std::cout << "input 0" << std::endl;
  // std::cout << test << std::endl;
  // int test2 = ((gr_complex *)input_items[1])->imag();
  // std::cout << "input 1" << std::endl;
  // std::cout << test2 << std::endl;

  
  // for (int i = 1; i < ninputs; i++) {
  //   // if( ((gr_complex *)input_items[i]) != input_items[i].end()){

  //   // }

  //   acc = acc + ((gr_complex *)input_items[i]);
  //   // int test = ((gr_complex *)input_items[i])->real();
  //   // std::cout << test << std::endl;
  // }
  // out[0] = *acc;
  // // Tell runtime system how many output items we produced.
  // return noutput_items;

    gr_complex* optr = (gr_complex*)output_items[0];
    int d_vlen =1;
    int ninputs = input_items.size();

    for (size_t i = 0; i < noutput_items * d_vlen; i++) {
        gr_complex acc = ((gr_complex*)input_items[0])[i];
        for (int j = 1; j < ninputs; j++){
            acc += ((gr_complex*)input_items[j])[i];
        }
        std::cout << "Input 0" <<  std::endl;
        std::cout << ((gr_complex*)input_items[0])[i].real() << std::endl;
        std::cout << "Input 1" <<  std::endl;
        std::cout << ((gr_complex*)input_items[1])[i].real() << std::endl;
        std::cout << "out" <<  std::endl;
        std::cout << acc.real() << std::endl;
        *optr++ = (gr_complex)acc;
    }
  return noutput_items;
}

} /* namespace lora_sdr */
} /* namespace gr */
