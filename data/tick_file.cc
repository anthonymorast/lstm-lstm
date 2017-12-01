
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <dirent.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <ctype.h>
#include <limits.h>
#include <time.h>

#include <data_rec.h>
#include <tick_file.h>

tick_file::tick_file(char *filename)
{  
  if((fd = open(filename,O_RDONLY)) < 0)
    {
      perror(filename);
      exit(1);
    }
  if(read(fd,&cur_data,sizeof(data_rec))!=sizeof(data_rec))
    {
      cur_data.time=LONG_MAX;
      cur_data.bid = 0.0;
      cur_data.ask = 0.0;
    }
}

data_rec tick_file::next_rec()
{
  data_rec rval = cur_data;
  if(rval.time == LONG_MAX)
    {
      printf("trying to read past eof\n");
      exit(1);
    }
  //  do{
    if(read(fd,&cur_data,sizeof(data_rec))!=sizeof(data_rec))
      {
	cur_data.time=LONG_MAX;
	cur_data.bid = 0.0;
	cur_data.ask = 0.0;
      }
    //}while((cur_data.time!=LONG_MAX)&&
    // ((cur_data.bid==0.0)||(cur_data.ask==0.0)));
  /* 
     if(cur_data.time == LONG_MAX)
     {
     printf("eof\n");
     exit(1);
     }
  */
  return rval;
}

// recursive routine to do binary search for a specified timestamp
// time is given in ms since January 1, 1970
void tick_file::position(int fd, off64_t left, off64_t right, time_t time)
{
  //printf("left=%ld right=%ld time=%ld\n",left,right,time/1000000);
  off64_t middle;

  //  printf("searching for time %ld\n",time);
  //  printf("left=%ld  right=%ld\n",left,right);

  if((right - left)<=sizeof(data_rec))
      //if(right==left)
    lseek64(fd,right,SEEK_SET);
  else
    {
      middle = left + ((right-left)>>1);
      middle = middle - (middle % sizeof(data_rec));
      lseek64(fd,middle,SEEK_SET);
      if((read(fd,&cur_data,sizeof(data_rec)))!=sizeof(data_rec))
	{
	  perror("error in seek");
	  exit(1);
	}
      //printf("left=%ld right=%ld time=%ld rectime=%ld\n",left,right,time/1000000,cur_data.time/1000000);

      if(cur_data.time < time)
	position(fd,middle,right,time);      
      else
	position(fd,left,middle,time);
    }
}

void tick_file::set_time(time_t time)
{
  off64_t left,right;
  // for each file, search for timestamp >= time, and
  // read in the record at that location.
  left = 0;
  right = lseek64(fd,0,SEEK_END);
  position(fd,left,right,time);
  if((read(fd,&cur_data,sizeof(data_rec)))!=sizeof(data_rec))
    {
	  perror("error in seek");
	  exit(1);
    }
  //printf("left=%ld right=%ld position=%ld\n",left,right,lseek64(fd,0,SEEK_CUR));
  //printf("cur_data.time=%ld  Searching for %ld\n",cur_data.time,time);
  //  printf("position=%ld  ",lseek64(fd,0,SEEK_CUR));
  //printf("cur_data.time=%ld  Searching for %ld\n",cur_data.time,time);

}

// void tick_file::position(int fd, off64_t left, off64_t right, time_t time)
// {
// }

// void tick_file::set_time(time_t time)
// {
//   int rval;

//   // lseek64(fd,0,SEEK_SET);  // probably not necessary
  
//   rval = sizeof(data_rec);
//   while((cur_data.time < time)&&(rval==sizeof(data_rec)))    
//     rval = read(fd,&cur_data,sizeof(data_rec));

//   if(rval != sizeof(data_rec))
//     {
//       perror("error in tick_file::set_time");
//       exit(1);
//     }
  
//   printf("position=%ld  ",lseek64(fd,0,SEEK_CUR));
//   printf("cur_data.time=%ld  Searching for %ld\n",cur_data.time,time);
  
// }

tick_file::~tick_file()
{
  close(fd);
}

