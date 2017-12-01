#include <dates.h>
#include <stdlib.h>

void fwrite_bits(FILE *f,int val,int nbit)
{
  int i;
  for(i=0;i<nbit;i++)
    {
      if(i==val)
	fprintf(f,"1 ");
      else
	fprintf(f,"0 ");
    }
}

void fprint_date(FILE *f,struct tm *t)
{
  int wday,mday;
  //fwrite_bits(f,t->tm_hour,24);
  fwrite_bits(f,t->tm_hour/6,4);
  fwrite_bits(f,t->tm_wday,5);
  //fwrite_bits(f,(t->tm_mday-1)/7,5);
}
int date_bitlen()
{
  return 9;
}

/* adjust t until it is on a sunday at 22:00 GMT */
time_t fix_to_sunday(time_t t)
{
  struct tm td, *tp;
  int done=0;
  do
    {
      tp = gmtime_r(&t,&td);
      if(tp==NULL)
	{
	  perror("error converting time");
	  exit(1);
	}
      if(td.tm_wday != 0)
	t += 60*60*24;
      else
	done=1;
    }
  while(!done);
  done=0;
  do
    {
      tp = gmtime_r(&t,&td);
      if(tp==NULL)
	{
	  perror("error converting time");
	  exit(1);
	}
      if(td.tm_hour != 22)
	t += 60*60;
      else
	done=1;
    }
  while(!done);
  tp = gmtime_r(&t,&td);
  td.tm_sec=0;
  return my_timegm(&td);
}

/* convert a (struct tm *) into a time_t, assuming
   tm is given in UTC (aka GMT)
*/
time_t my_timegm(struct tm *tim)
{
  time_t ret;
  char *tz;

  tz = getenv("TZ");
  setenv("TZ", "", 1);
  tzset();
  ret = mktime(tim);
  if (tz)
    setenv("TZ", tz, 1);
  else
    unsetenv("TZ");
  tzset();
  return ret;
}

/* verify that the string is made up only of digits */
void checknum(string s,int len)
{
  int i;
  for(i=0;i<s.length();i++)
    if((s.length()!=len) || !isdigit(s[i]))
      {
        printf("date must be MM/DD/YYYY:HH:MM\n");
        exit(1);
      }
}

/* Convert a string MM/DD/YYYY into time_t, assuming
   that MM/DD/YYYY is given in UTC (aka GMT). 
*/
time_t my_getdate(string d)
{
  struct tm td;
  time_t t;
  if(d.length()!=16)
    {
      printf("dates must be given as MM/DD/YYYY:HH:MM\n");
      exit(1);
    }
  string mst = d.substr(0,2);
  string dst = d.substr(3,2);
  string yst = d.substr(6,4);
  string tmh = d.substr(11,2);
  string tmm = d.substr(14,2);
  checknum(mst,2);
  checknum(dst,2);
  checknum(yst,4);
  checknum(tmm,2);
  checknum(tmh,2);
  td.tm_sec = 0;
  td.tm_min = atoi(tmm.c_str());
  td.tm_hour = atoi(tmh.c_str());
  td.tm_mday = atoi(dst.c_str());
  td.tm_mon = atoi(mst.c_str())-1;
  td.tm_year = atoi(yst.c_str()) - 1900;
  td.tm_wday = 0;
  td.tm_yday = 0;
  //td.tm_isdst = -1;
  td.tm_isdst = 0;

  return my_timegm(&td);
}

/* This routine is to take care of "leap seconds."
   Convert t to broken-down time, make sure secs 
   are zero, and convert it back. It's probably not
   even necessary. */
time_t round_date(time_t t)
{
  struct tm *gmt;
  gmt = gmtime(&t);
  if(gmt->tm_sec != 0)
    {
      printf("rounding leap second %d\n",gmt->tm_sec);
      gmt->tm_sec = 0;
    }
  t = my_timegm(gmt);
  return t;
}


