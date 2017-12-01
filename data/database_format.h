
/* This is the intermediate database format.  We eventually convert it to
   the data_rec format */

#ifndef DATABASE_FORMAT_H
#define DATABASE_FORMAT_H

#include <time.h>

typedef struct{
  unsigned long serial;
  time_t time;
  float ask;
  float bid;
}datarec;


#endif
