#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <time.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <data_rec.h>

int main(int argc, char **argv)
{
  int fd;
  data_rec d;
  time_t t;

  if(argc!=2)
    {
      printf("usage: %s <filename>\n",argv[0]);
      exit(1);
    }
  
  if((fd=open(argv[1],O_RDONLY))<0)
    {
      printf("%s: unable to open %s for input\n",argv[0],argv[1]);
      exit(1);
    }


  while(read(fd,&d,sizeof(data_rec))==sizeof(data_rec))
    {
      t = d.time/1000;
      printf("%s %ld %10f %10f\n",asctime(gmtime(&t)),d.time,d.bid,d.ask);
    }
}
/*
Fri Jan  3 16:37:04 2003
 1041633424000000   1.563200   1.563700
Sun Jan  5 17:03:29 2003
 1041807809000000   1.563700   1.564200
*/

