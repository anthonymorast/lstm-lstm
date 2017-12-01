
#include <data_rec.h>
#include <tick_file.h>
#include <stdio.h>
#include <time.h>
#include <dates.h>

using namespace std;

#define SECS 3600

int main(int argc, char **argv)
{

  if(argc != 2)
    {
      printf("Usage: %s <filename>\n",argv[0]);
      return -1;
    }

  //  time_t start = my_getdate("01/05/2003 22:00");

  tick_file t(argv[1]);
  data_rec prev,cur;
  time_t tmp_time;
  struct tm prev_time;
  struct tm cur_time;
  int state,begin_weekend,end_weekend;
  
  cur = t.next_rec();

  while(t.more_ticks())
    {
      prev = cur;
      cur = t.next_rec();

      if((cur.time - prev.time) > ((SECS*1000)+100000))
	{
	  // four cases:
	  // 1) Normal weekend gap
	  //    check to see if prev was on a Friday, after 21:00 and
	  //    cur was on Sunday before 23:00

	  // 2) Gap did not include a weekend

	  // 3) Gap includes, but not limited to a weekend (really two gaps)
	  //    a) Gap started before start of normal weekend gap
	  //       and ends at start of normal weekend gap, and/or
	  //    b) Gap started at end of weekend and extended into the start
          //       of the week.

	  tmp_time = prev.time/1000;
	  gmtime_r(&tmp_time,&prev_time);
	  if((prev_time.tm_wday==5)&&(prev_time.tm_hour>=21))
	    begin_weekend = 1;
	  else
	    begin_weekend = 0;

	  tmp_time = cur.time/1000;
	  gmtime_r(&tmp_time,&cur_time);
	  if((cur_time.tm_wday==0)&&(cur_time.tm_hour<=22))
	    end_weekend = 1;
	  else
	    end_weekend = 0;

// 	  printf("%d %d - %d ; %d %d - %d\n",
// 		 prev_time.tm_wday,prev_time.tm_hour,begin_weekend,
// 		 cur_time.tm_wday,cur_time.tm_hour,end_weekend);

	  state = (begin_weekend << 1) + end_weekend;
	  switch (state)
	    {
	    case 0:
	      // check te see if it spanned a weekend
	    case 1:
	      // missed data at beginning of week	      
	    case 2:
	      // missed data at end of week
	      printf("%ld %ld\n",prev.time/1000,cur.time/1000);

 	      tmp_time = prev.time/1000;
 	      printf("Gap from: %s",asctime(gmtime(&tmp_time)));
	      	      
 	      tmp_time = cur.time/1000;
 	      printf("      to: %s",asctime(gmtime(&tmp_time)));	      
	      break;

	    case 3:
	      // began and ended at normal weekend times
	      break;
	    }

	}

      
    }


  return 0;
}
