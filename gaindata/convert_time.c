/* 
   Convert the intermediate file format that was used in
   the sorting operation to the final file format.  
   Look for, and delete, strange values as we go.
*/

#include <math.h>

#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <dirent.h>
#include <time.h>
#include <database_format.h>
#include <data_rec.h>

int printrec(datarec *rec)
{
  printf("time:%ld - %f %f\n",rec->time,rec->ask,rec->bid);
}


int sample_OK(float curr,float ave)
{
  float min;
  if(curr<ave)
    min = curr;
  else
    min = ave;

  if((fabs(curr-ave) < (0.25 * min))&&(min > 0.0))
    return 1;
  return 0;
}

/* maximum number of identical times that we can handle */
#define MAX_IDENT 1024

int convert(char *filename,char *ofilename)
{
  FILE *src;
  FILE *dst;
  static datarec rec[MAX_IDENT];
  data_rec outrec;
  int numident;
  int valid = 1;
  int write_last = 1;
  int i;

  float ask_ave,bid_ave;
  int firstval=1;
  int num_bad;

  int verbose = 0;
  
  if((src=fopen(filename,"r"))==NULL)
    {
      perror(filename);
      exit(1);
    }
  if((dst=fopen(ofilename,"w"))==NULL)
    {
      perror(ofilename);
      exit(1);
    }

  int bad_sample;

  /* read first tick to position 0 */
  if((valid=fread(&(rec[0]),sizeof(datarec),1,src)) == 1)
    {
      ask_ave=rec[0].ask;
      bid_ave=rec[0].bid;
      num_bad=0;
      /* loop: */
      /*   read next tick to position 1 */
      do
	{
	  valid = (fread(&(rec[1]),sizeof(datarec),1,src) == 1);
	  /* check to make sure ask and bid prices are not wierd */
	  bad_sample = !(sample_OK(rec[1].ask,ask_ave)||
			 sample_OK(rec[1].bid,bid_ave));
	  if(bad_sample)
	    {
	      num_bad++;
	      if(verbose)
		{
		  printf("removing sample %ld %f %f - ",
			 rec[1].time,
			 rec[1].bid,
			 rec[1].ask);
		  printf("averages %f %f\n",bid_ave,ask_ave);
		}
	    }
	  //else
	  //{
	  ask_ave = (ask_ave+2*rec[1].ask)/3.0;
	  bid_ave = (bid_ave+2*rec[1].bid)/3.0;
	  //}
	}
      while(bad_sample&&valid);

      while(valid)
	{
	  /* at this point, we always have ticks in position 0 and 1 */
	  /* keep adding ticks until time changes or eof */
	  numident = 1;
	  while(valid&&( rec[numident-1].time == rec[numident].time))
	    {
	      do
		{
		  valid=(fread(&(rec[numident+1]),sizeof(datarec),1,src) == 1);
		  /* check to make sure ask and bid prices are not weird */
		  bad_sample = !(sample_OK(rec[numident+1].ask,ask_ave)||
				 sample_OK(rec[numident+1].bid,bid_ave));

		  if(bad_sample)
		    {
		      num_bad++;
		      if(verbose)
			{
			  printf("removing sample %ld %f %f - ",
				 rec[numident+1].time,
				 rec[numident+1].bid,
				 rec[numident+1].ask);
			  printf("averages %f %f\n",bid_ave,ask_ave);
			}
		    }
		  //else
		  //{
		  ask_ave = (ask_ave+rec[numident+1].ask)/2.0;
		  bid_ave = (bid_ave+rec[numident+1].bid)/2.0;
		  //  }
		}
	      while(bad_sample&&valid);
	      

	      if(valid)
		numident++;
	      else
		write_last = 0;
	    }
 	  if(numident>1000) 
 	    { 
 	      printf("numident=%d\n",numident); 
 	      for(i=0;i<numident;i++) 
 		printrec(&rec[i]); 
 	    } 

	  /* now we have at least two valid ticks, and maybe more */
	  /* write record 0 through numident-1 (all the ones with same
	     time stamp) */
	  for(i=0;i<numident;i++)
	    {
	      outrec.ask = rec[i].ask;
	      outrec.bid = rec[i].bid;
	      outrec.time = rec[i].time*1000 + i*(1000.0/numident);
	      if(fwrite(&outrec,sizeof(data_rec),1,dst) != 1)
		{
		  perror("unable to write output");
		  exit(1);
		}
	    }
	  /*   move record numident to 0 */
	  if(valid)
	    {
	      rec[0] = rec[numident];
	      do
		{
		  valid = (fread(&(rec[1]),sizeof(datarec),1,src) == 1);
		  bad_sample = !(sample_OK(rec[1].ask,ask_ave)||
				 sample_OK(rec[1].bid,bid_ave));
		  if(bad_sample)
		    {
		      num_bad++;
		      if(verbose)
			{
			  printf("removing sample %ld %f %f - ",
				 rec[1].time,
				 rec[1].bid,
				 rec[1].ask);
			  printf("averages %f %f\n",bid_ave,ask_ave);
			}
		    }
		  // else
		  // {
		  ask_ave = (ask_ave+rec[1].ask)/2.0;
		  bid_ave = (bid_ave+rec[1].bid)/2.0;
		  //}
		}
	      while(bad_sample&&valid);
	    }
	  else
	    write_last = 0;
	}
      if(write_last)
	{
	  outrec.ask = rec[0].ask;
	  outrec.bid = rec[0].bid;
	  outrec.time = rec[0].time*1000;
	  if(fwrite(&outrec,sizeof(data_rec),1,dst) != 1)
	    {
	      perror("unable to write output");
	      exit(1);
	    }
	}
      printf("  final time: %ld\n",outrec.time);
    }
  fclose(src);
  fclose(dst);
  return num_bad;
}


int main()
{
  char dirname[128];
  char odirname[128];
  char filename[128];
  char ofilename[128];
  int year,month;
  char command[128];
  DIR *d;
  struct dirent *de;
  int dupts = 0;

  sprintf(dirname,"data.reorganized");
  sprintf(odirname,"data.final");

  printf("datarec size is %ld\ndata_rec size is %ld\n",
	 sizeof(datarec),sizeof(data_rec));
  printf("time_t size is %ld\nint64_t size is %ld\n",
	 sizeof(time_t),sizeof(int64_t));
  printf("int size is %ld\nunsigned int size is %ld\n",
	 sizeof(int),sizeof(unsigned int));

  if((d = opendir(dirname))==NULL)
    {
      perror(dirname);
      exit(1);
    }
  /* read all entries, looking for data files */
  while((de=readdir(d))!=NULL)
    {
      if(de->d_name[0]!='.')
	{
	  sprintf(filename,"%s/%s",dirname,de->d_name);
	  sprintf(ofilename,"%s/%s",odirname,de->d_name);
	  printf("converting %s  ",filename);
	  printf("%d suspicious records removed\n",
		 convert(filename,ofilename));
	}
    }
  closedir(d);
  
  
  return 0;
}




