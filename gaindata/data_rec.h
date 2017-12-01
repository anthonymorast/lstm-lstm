
/* this is the final format for the tick database */
#ifndef DATA_REC_H
#define DATA_REC_H

#include<sys/types.h>

typedef struct{
  /* microseconds since Unix Epoch */
  int64_t time; 
  float ask;
  float bid;
}data_rec;


#endif
