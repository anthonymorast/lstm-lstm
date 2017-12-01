
#ifndef TICK_FILE_H
#define TICK_FILE_H

#include <limits.h>
#include <data_rec.h>

#define DEFAULT_DIR (char *)"../data/data.final"

class tick_file{
private:
  int fd;
  data_rec cur_data;
  void position(int i, long int left, long int right, time_t time);

public:
  tick_file(){}
  tick_file(char* filename);
  ~tick_file();
  data_rec next_rec();
  time_t get_time(){return cur_data.time/1000;}
  void set_time(time_t time);
  int more_ticks(){return (cur_data.time<LONG_MAX);}
};
  
#endif
