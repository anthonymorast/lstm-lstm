/* a quick and dirty program to unpack the files downloaded from
   gaincapital.com extract the data, and put it into separate files
   for each symbol pair.
   
*/

/* 2004/05/GBP_USD_Week2.zip - file is messed up*/

/* 2004/10/USD_CAD_Week3 seems to have a problem */

/* 2005/05/AUD_JPY_Week2.zip - has lots of extra files in it */

/* 2007/08  *Week5.zip unzips to *Week1.csv.  Run the fix script */
/* 2007/11  *Week5.zip unzips to *Week1.csv.  Run the fix script */
/* 2009/02  GBP_JPY_Week3.csv - last line is messed up.  Run the fix script */

#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <dirent.h>
#include <time.h>
#include <database_format.h>

char *outfiledir="data.reorganized";

int printrec(datarec *rec)
{
  printf("time:%ld - %f %f",rec->time,rec->ask,rec->bid);
}


#define LINE_MAX 256


char *unicode_fgets(char *s, int size, FILE *f)
{
  unsigned char tmp[2];
  int endofline=0;
  int i = 0;
  while(!feof(f)&&!endofline)
    {
      if( fread(tmp,1,2,f) == 2)
	{
	  s[i++] = tmp[0];
	  if((i == (size-1))||(tmp[0] == '\n'))
	    endofline=1;
	  /*	  printf("%d %c\n",tmp[0],tmp[0]); */
	}
      else
	endofline=1;
    }
  s[i] = 0;
  if((i>0)||(!feof(f)))
    return s;
  return NULL;
}


void copy_data(FILE *infile,FILE *outfile,char *infilename)
{
  char *serial,*pair;
  char *yr,*mo,*dy,*hr,*mn,*sc;
  char *ask;
  char *bid;
  char *junk;
  char line[LINE_MAX];
  char oline[LINE_MAX];
  struct tm b_time;
  int unicode;
  char *result;
  datarec rec;
  char *linecopy;


  /* check to see if it is unicode */
  unsigned char tmp[2];
  if( fread(tmp,1,2,infile) != 2)
    {
      printf("Empty file!");
      exit(1);
    }
  if((tmp[0] == 0xFF)&&(tmp[1] == 0xFE))
    {
      printf("This looks like a Unicode file\n");
      unicode = 1;
    }
  else
    {
      unicode = 0;
      if(fseek(infile, 0, SEEK_SET)!=0)
	{
	  printf("Seek failed\n");
	  exit(1);
	}
    }

  while(!feof(infile))
    {
      /* get one line at a time and parse it */
      if(unicode)
	result=unicode_fgets(line,LINE_MAX,infile);
      else
	result=fgets(line,LINE_MAX,infile);
	
      if((result!=NULL)&&(strlen(line)>10))
	{

	  /* trim cr and/or lf off end of line */
	  /* not really necessary, but good practice */
	  while((line[strlen(line)-1]=='\n')||(line[strlen(line)-1]=='\r'))
	    line[strlen(line)-1]=0;

	  linecopy=strdup(line);

	  
	  /* the line better be in the proper format, or we will get a
	     segfault 
	  */

	  serial = line;
	  /*
		With new data, the column order has switched so junk (cDealable) is in 
		the second column rather than the last. Move this to compensate for that.
	  */
	  junk = strchr(serial, ',');
	  if (junk != NULL) {
	    *(junk++) = 0;
	  //pair = strchr(serial,',');
	  pair = strchr(junk, ',');
	  if(pair!=NULL) {
	    *(pair++) = 0;
	    yr = strchr(pair,',');
	    if(yr!=NULL) {
	      *(yr++) = 0;
	      mo = strchr(yr,'-');
	      if(mo!=NULL) {
		*(mo++) = 0;
		dy = strchr(mo,'-');
		if(dy!=NULL) {
		  *(dy++) = 0;
		  hr = strchr(dy,' ');
		  if(hr!=NULL) {
		    *(hr++) = 0;
		    mn = strchr(hr,':');
		    if(mn!=NULL) {
		      *(mn++) = 0;
		      sc = strchr(mn,':');
		      if(sc!=NULL) {
			*(sc++) = 0;
			bid = strchr(sc,',');
			if(bid!=NULL) {
			  *(bid++) = 0;
			  while((!isdigit(*bid))&&(*bid != '.'))
			    bid++;
			  ask = strchr(bid,',');
			  if(ask!=NULL) {
			    *(ask++) = 0;
			    while((!isdigit(*ask))&&(*ask != '.'))
			      ask++;
			    //junk = strchr(ask,',');
			    //if(junk!=NULL) {
			    //  *(junk++) = 0; 
			      rec.serial = (unsigned long)atol(serial);
			      
			      /* convert time, which is given in EST 
				 without dst, to number of seconds 
				 since January 1, 1970, UTC, for much
				 more efficient storage and manipulation  */
			      b_time.tm_year = atoi(yr)-1900;
			      if(b_time.tm_year < 0)
				{
				  printf("Year less than zero: %d\n",
					 b_time.tm_year);
				  continue;
				  }
			      b_time.tm_mon = atoi(mo)-1;
			      b_time.tm_mday = atoi(dy);
			      b_time.tm_hour = atoi(hr);
			      b_time.tm_min = atoi(mn);
			      b_time.tm_sec = atoi(sc);
			      b_time.tm_isdst = 0;
			      
			      /* we previously set our timezone 
				 info to New York time */
			      rec.time = mktime(&b_time);
			      if((rec.time>time(NULL))||(rec.time<0))
				{
				  printf("ridiculous time value\n");
				  printf("yr=%s mo=%s dy=%s hr=%s mn=%s sc=%s\n",yr,mo,dy,hr,mn,sc);
				  printf("%s",asctime(&b_time));
				  printf("file: %s\n",infilename);
				  exit(1);
				}
			      /* convert ask and bid prices to float 
				 for more efficient storage and 
				 manipulation. atof needs it to not 
				 start with '.' */
			      char fixfloat[128];
			      
			      sprintf(fixfloat,"0%s",ask);
			      rec.ask = atof(fixfloat);
			      
			      sprintf(fixfloat,"0%s",bid);
			      rec.bid = atof(fixfloat);

			      /* write the data efficiently */
			      if(fwrite(&rec,sizeof(datarec),1,outfile) != 1)
				{
				  perror("unable to write to output file");
				  exit(1);
				}
			      /* make sure what we wrote was what we read */
			      sprintf(oline,"%ld,%s,%02d-%02d-%02d %02d:%02d:%02d,%s,%s,%s",				      
				      rec.serial,
				      pair,
				      b_time.tm_year-100,
				      b_time.tm_mon,
				      b_time.tm_mday,
				      b_time.tm_hour,
				      b_time.tm_min,
				      b_time.tm_sec,
				      bid,
				      ask,
				      junk);
			      if(!strcmp(oline,line))
				{
				  printf("read : %s\nwrote: %s\n",line,oline);
				  exit(1);
				}
			    }
			  }
			}
		      }
		    }
		  }
		}
	      }
	    }
	  }
	  free(linecopy);
	}
    }
}


void processfile(char *dirname,char *fname)
{
  char *newname = strdup(fname);
  char *targetname = strdup(fname);
  char destpath[128];
  char sourcepath[128];
  char othersourcepath[128];
  char command[128];
  int i;
  FILE *infile;
  FILE *otherinfile;
  FILE *outfile;
  datarec rec;

  /* convert the ASCII or Unicode file to a more efficient binary file */
  /* <dirname>/<fname> is the input file
     <outfiledir>/<targetname> is what we want the data appended to
  */
  for(i=3;i<6;i++)
    targetname[i]=targetname[i+1];
  targetname[6]=0;

  sprintf(sourcepath,"%s/%s",dirname,newname);
  sprintf(destpath,"%s/%s",outfiledir,targetname);

  if((infile = fopen(sourcepath,"r"))==NULL)
    {
      sprintf(command,"Unable to open %s",sourcepath);
      perror(command);
      exit(1);
    }
  if((outfile = fopen(destpath,"a"))==NULL)
    {
      sprintf(command,"Unable to open %s",destpath);
      perror(command);
      exit(1);
    }
  printf("Processing file %s into file %s\n",sourcepath,destpath);

  copy_data(infile,outfile,sourcepath);
  
  fclose(infile);
  fclose(outfile);
  
  free(newname);
  free(targetname);

}


int main()
{
  char dirname[32];
  char zippath[32];
  int year,month;
  char command[128];
  DIR *d;
  struct dirent *de;

  /* make sure destination dir is there and that it is empty */
  sprintf(command,"mkdir %s",outfiledir);
  system(command);

  sprintf(command,"rm -f %s/*",outfiledir);
  system(command);

  /* Fool the time function library into thinking we are in New York,
     where the Gain Capital data was timestamped. Hopefully, this will
     cause mktime to work the way it should, and we can convert all of
     the timestamps to seconds since the Unix Epoch, which is defined
     precisely as 00:00:00 UTC on January 1, 1970, not counting leap
     seconds. */
  setenv("TZ", ":/usr/share/zoneinfo/America/New_York", 1);
  tzset();
  
  for(year=2003;year<2018;year++)
    for(month=1;month<13;month++)
      {
	sprintf(dirname,"%4d/%02d",year,month);
	/* open the directory for this year/month */
	printf("Processing directory %s\n",dirname);
	/* delete any .csv files in the dir */
	sprintf(command,"rm -f %s/*.csv",dirname);
	system(command);
	d = opendir(dirname);
	if(d!=NULL)
	  {
	    /* read all entries, looking for zip files */
	    while((de=readdir(d))!=NULL)
	      {
		printf("checking file %s\n",de->d_name);
		if(strstr(de->d_name,".zip")!=NULL)
		  { /* unzip files */
		    sprintf(zippath,"%s/%s",dirname,de->d_name);
		    sprintf(command,"unzip -n -d %s %s",dirname, zippath);
		    system(command);
		    /* fixup the filename */
		    de->d_name[strlen(de->d_name)-3]='c';
		    de->d_name[strlen(de->d_name)-2]='s';
		    de->d_name[strlen(de->d_name)-1]='v';
		  }

		/* make sure the resulting file ends in ".csv" */
		sprintf(command,"find %s -name \\*.CSV -exec ./fixextension \\{\\} \\;",dirname); 
		system(command); 

		/* now add the data to our database */
		if(strstr(de->d_name,".csv")!=NULL)
		  {
		    processfile(dirname,de->d_name);
		    /* now gzip the file */
		    /* sprintf(zippath,"%s/%s",dirname,de->d_name); */
		    /* sprintf(command,"gzip %s",zippath); */
		    /* system(command); */
		    sprintf(command,"%s/%s",dirname,de->d_name);
		    unlink(command);
		  }
	      }
	    closedir(d);
	  }
      }
  return 0;
}




