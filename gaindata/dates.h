#ifndef DATES_H
#define DATES_H

#include <time.h>
#include <string>
#include <stdio.h>

using namespace std;

/* convert a (struct tm *) into a time_t, assuming
   tm is given in UTC (aka GMT)
*/
time_t my_timegm(struct tm *tim);



/* Convert a string MM/DD/YYYY into time_t, assuming
   that MM/DD/YYYY is given in UTC (aka GMT). 
*/
time_t my_getdate(string d);

/* This routine is to take care of "leap seconds."
   Convert t to broken-down time, make sure secs 
   are zero, and convert it back. It's probably not
   even necessary. */
time_t round_date(time_t t);

void fprint_date(FILE *f,struct tm *t);

/* adjust t until it is on a sunday at 21:00 GMT */
time_t fix_to_sunday(time_t t);
int date_bitlen();

#endif
