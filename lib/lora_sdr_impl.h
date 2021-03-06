/* -*- c++ -*- */
/*
 * Copyright 2020 "Martyn van Dijke".
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_LORA_SDR_LORA_SDR_IMPL_H
#define INCLUDED_LORA_SDR_LORA_SDR_IMPL_H

#include <lora_sdr/lora_sdr.h>

namespace gr {
namespace lora_sdr {

class lora_sdr_impl : public lora_sdr {
private:
  // Nothing to declare in this block.

public:
  /**
   * @brief Construct a new lora sdr impl object
   * 
   */
  lora_sdr_impl();
  /**
   * @brief Destroy the lora sdr impl object
   * 
   */
  ~lora_sdr_impl();

  /**
   * @brief 
   * 
   * @param noutput_items 
   * @param ninput_items_required 
   */
  void forecast(int noutput_items, gr_vector_int &ninput_items_required);

  /**
   * @brief 
   * 
   * @param noutput_items 
   * @param ninput_items 
   * @param input_items 
   * @param output_items 
   * @return int 
   */
  int general_work(int noutput_items, gr_vector_int &ninput_items,
                   gr_vector_const_void_star &input_items,
                   gr_vector_void_star &output_items);
};

} // namespace lora_sdr
} // namespace gr

#endif /* INCLUDED_LORA_SDR_LORA_SDR_IMPL_H */
