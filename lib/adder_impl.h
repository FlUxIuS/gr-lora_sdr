/**
 * @file adder_impl.h
 * @author Martyn van Dijke (martijnvdijke600@gmail.com)
 * @brief 
 * @version 0.1
 * @date 2021-01-12
 * 
 * 
 */
#ifndef INCLUDED_LORA_SDR_ADDER_IMPL_H
#define INCLUDED_LORA_SDR_ADDER_IMPL_H

#include <lora_sdr/adder.h>

namespace gr {
  namespace lora_sdr {

    class adder_impl : public adder
    {
     private:
      // Nothing to declare in this block.

     public:
      adder_impl();
      ~adder_impl();

      // Where all the action really happens
      int work(
              int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items
      );
    };

  } // namespace lora_sdr
} // namespace gr

#endif /* INCLUDED_LORA_SDR_ADDER_IMPL_H */

