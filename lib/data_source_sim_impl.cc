/**
 * @file data_source_sim_impl.cc
 * @author Martyn van Dijke (martijnvdijke600@gmail.com)
 * @brief
 * @version 0.1
 * @date 2021-01-08
 *
 *
 */
#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "data_source_sim_impl.h"
#include <gnuradio/io_signature.h>
#include <lora_sdr/utilities.h>
#include <unistd.h>

// Fix for libboost > 1.75
#include <boost/bind/placeholders.hpp>
using namespace boost::placeholders;

namespace gr {
namespace lora_sdr {

data_source_sim::sptr data_source_sim::make(int pay_len, int n_frames,
                                            std::string string_input,
                                            uint32_t mean, bool multi_control) {
  return gnuradio::get_initial_sptr(new data_source_sim_impl(
      pay_len, n_frames, string_input, mean, multi_control));
}

/**
 * @brief Construct a new data source impl object
 *
 * @param pay_len : payload length
 * @param n_frames : number of frames to generate data for
 * @param string_input : input string from gnuradio-companian
 */
data_source_sim_impl::data_source_sim_impl(int pay_len, int n_frames,
                                           std::string string_input,
                                           uint32_t mean, bool multi_control)
    : gr::block("data_source", gr::io_signature::make(0, 0, 0),
                gr::io_signature::make(0, 1, sizeof(uint8_t))) {
  m_n_frames = n_frames;
  m_pay_len = pay_len;
  frame_cnt = 0; // let some time to the Rx to start listening
  m_string_input = string_input;
  m_mean = mean;
  m_multi_control = multi_control;
  m_finished = false;
  m_finished_wait = false;
  message_port_register_in(pmt::mp("ctrl_in"));
  // set msg handler for the input port to be the ctrl_in_handler
  set_msg_handler(pmt::mp("ctrl_in"),
                  [this](pmt::pmt_t msg) { this->ctrl_in_handler(msg); });
  message_port_register_out(pmt::mp("msg"));
  set_thread_priority(1);
}

/**
 * @brief Destroy the data source impl object
 *
 */
data_source_sim_impl::~data_source_sim_impl() {}

/**
 * @brief Random string generator as input data for the flowgraph
 *
 * @param Nbytes : number of bytes
 * @return std::string : the random generated data string
 */
std::string data_source_sim_impl::random_string(int Nbytes) {
  const char *charmap =
      "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  const size_t charmapLength = strlen(charmap);
  auto generator = [&]() { return charmap[rand() % charmapLength]; };
  std::string result;
  result.reserve(Nbytes);
  std::generate_n(std::back_inserter(result), Nbytes, generator);
  return result;
}

void data_source_sim_impl::ctrl_in_handler(pmt::pmt_t msg) {
  std::cout << "Got a message from control multi" << std::endl;
  m_finished = true;
  m_finished_wait = true;
  std::cout << m_finished << std::endl;
}

/**
 * @brief Place holder function does not do anything for the data source.
 *
 * @param noutput_items
 * @param ninput_items_required
 */
void data_source_sim_impl::forecast(int noutput_items,
                                    gr_vector_int &ninput_items_required) {
  /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
}

/**
 * @brief Main function, generates random ([a-z A-Z
 * 0-9]) data input to be sent over the network or if input_string set send this
 * over the network. The sim version of the data_source has an internal sleep
 * function set by the parameter mean
 *
 * @param noutput_items : number of output items : 1
 * @param ninput_items : number of input items : 0
 * @param input_items : input item : 0
 * @param output_items : ooutput items :
 * @return int : work status
 */
int data_source_sim_impl::general_work(int noutput_items,
                                       gr_vector_int &ninput_items,
                                       gr_vector_const_void_star &input_items,
                                       gr_vector_void_star &output_items) {
  // if we are not finished, generate data frames
  if (m_finished_wait == false) {

    // if the number of frames send is less then the number of frames that must
    // be send
    while (frame_cnt < m_n_frames + 1) {
      // variable to hold string input
      std::string str;

      // if no string is set generate random string otherwise use set string.
      if (m_string_input.empty()) {
        // generate random string
        str = random_string(m_pay_len);
      } else {
        // take input string
        str = m_string_input;
      }
      // TODO fix +1 bug ?
#ifdef GRLORA_DEBUG
      // output data string
      GR_LOG_DEBUG(this->d_logger, "DEBUG:Input string:" + str);
#endif
      // send string over pmt port "msg" to neighboors
      message_port_pub(pmt::intern("msg"), pmt::mp(str));
      // print once in every 50 frames information about the number of frames
      if (!mod(frame_cnt, 50)) {
        GR_LOG_INFO(this->d_logger,
                    "INFO:Processing frame :" + std::to_string(frame_cnt) +
                        "/" + std::to_string(m_n_frames));
      }
      // let this thread sleep for the inputted mean time.
      boost::this_thread::sleep(boost::posix_time::milliseconds(m_mean));
      frame_cnt++;
      return 2 * m_pay_len;
    }
    // if the number of frames is the same -> all frames are sent
    if (frame_cnt > m_n_frames) {
      GR_LOG_INFO(this->d_logger,
                  "INFO:Done with generating data packets!, generated : " +
                      std::to_string(m_n_frames) + " frames");
      //
      boost::this_thread::sleep(boost::posix_time::milliseconds(m_mean));
      if (m_multi_control == true) {
        // tag the end of the Tx stream
        add_item_tag(0, nitems_written(0), pmt::intern("status"),
                     pmt::intern("done"));
      }
      // set internal sate to done, no more messages should be produced
      m_finished_wait = true;
#ifdef GRLORA_DEBUG
      GR_LOG_DEBUG(this->d_logger,
                   "DEBUG:Work done!\nNo more new data packets, data packets "
                   "will be processed and program will exit thereafter...");
#endif
      std::cout << m_finished_wait << std::endl;
            std::cout << m_finished << std::endl;
      std::cout << m_multi_control << std::endl;

      return 1;
    } else {
      GR_LOG_DEBUG(this->d_logger,
                   "DEBUG:Something wrong in sending the frames to the blocks");
      return 0;
    }
  }
  if (m_finished_wait == true && m_finished == false &&
      m_multi_control == false){
        
        boost::this_thread::sleep(boost::posix_time::milliseconds(m_mean));
      }
  if (m_finished_wait == true && m_finished == false &&
      m_multi_control == true) {
    boost::this_thread::sleep(boost::posix_time::milliseconds(m_mean));
          std::cout << "Tagging end of the stream"<< std::endl;

    // tag the end of the Tx stream
    add_item_tag(0, nitems_written(0), pmt::intern("status"),
                 pmt::intern("done"));
    return 1;
  }
  if (m_finished == true) {
    std::cout << "Sending work_done to blocks" << std::endl;
    std::cout << m_finished << std::endl;
    //return 1;
    return WORK_DONE;
  }
}

} /* namespace lora_sdr */
} /* namespace gr */
