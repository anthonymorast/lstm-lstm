/* 
	a quick and dirty program to download zipped csv files 
	from gaincapital.com, fix their names to be more Unix
   	friendly, and convert them to gnuzipped csv files. 
*/


#include <stdlib.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>


/* skip downloading:
/* 2004/05/GBP_USD_Week2.zip - file is messed up*/

void parse_cmd(int argc, char* argv[], int *start, int *end);


char *monthdirs[]={"01\\ January","02\\ February","03\\ March",
		   "04\\ April","05\\ May","06\\ June",
		   "07\\ July","08\\ August","09\\ September",
		   "10\\ October","11\\ November","12\\ December"};


#define TMPSIZE 1024

int main(int argc, char* argv[])
{

	char yeardir[6];
	int year,month;
  	char command[256];
  	FILE *infile,*outfile;
  	char tmpstr[TMPSIZE];
  	char *slash;

	int start, end;
	parse_cmd(argc, argv, &start, &end);
	printf("%d, %d", start, end);
  
  	/* Download index.html for each year and month, 
     	and parse them into lists of the files to be downloaded.
    	create the subdirectory structure as we go.
  	*/
  	for(year=start;year<=end;year++)
  	{
  		sprintf(yeardir,"%4d",year);
    	for(month=0;month<12;month++)
		{
			unlink("index.html");
	  		/* use wget to download index.html from the desired directory */
	  		sprintf(command,"wget http://ratedata.gaincapital.com/%s/%s/", yeardir,monthdirs[month]);
	  		printf("%s\n",command);
	  		if(system(command) == 0)
	    	{
	      		/* use sed to parse index.html into a list of files to get */
	      		sprintf(command,"grep zip index.html | sed \"s/^.*href=\\\"/http:\\/\\/ratedata\\.gaincapital\\.com\\/%s\\/%s\\//\"  | sed \"s/\\\".*//\" | grep -v align > filelist.tmp",
						yeardir,monthdirs[month]);
		      	printf("%s\n",command);
		      	system(command);

		      	/* fix up the filenames */
		      	if((outfile = fopen("filelist","w"))!=NULL)
				{
			  		if((infile = fopen("filelist.tmp","r"))!=NULL)
			    	{
			      		while(fgets(tmpstr,TMPSIZE,infile)>0)
						{
				  			printf("%s",tmpstr);
				  			if((slash=strchr(tmpstr,'\\'))!=NULL)
				    		{
				      			*(slash-1) = 0;
				      			fprintf(outfile,"%s%s",tmpstr,slash+1);
				      			printf("%s%s",tmpstr,slash+1);
				    		}		   
						}	 
			      		fclose(infile);
			    	}
			  		fclose(outfile);
				}
		      	unlink("filelist.tmp");
	
		      	/* create subdirectory to hold the files */
		      	mkdir(yeardir,0700);
		      	sprintf(command,"%s/%02d",yeardir,month+1);
		      	mkdir(command,0700);
	
		      	/* move the file list into the subdirectory */
		      	sprintf(command,"%s/%02d/filelist",yeardir,month+1);
		      	unlink(command);
		      	link("filelist",command);
		      	unlink("filelist");
		      	unlink("index.html");
	
		      	/* go there and download */
		      	sprintf(command,"%s/%02d",yeardir,month+1);
		      	chdir(command);
	
		      	/*sprintf(command,"wget -N -r -i filelist "); */
		      	/*sprintf(command,"wget --no-clobber -i filelist "); */
		      	sprintf(command,"wget -c -i filelist ");
		      	system(command);
	
				/*sprintf(command,"find . -name \\*.zip -exec unzip -u -o \\{\\} \\;"); system(command); */
	
				/* 	      /\* if we delete the original zip file, wget will download */
				/* 		 it again every time we re-run this program *\/ */
				/* /\* 	      sprintf(command,"find . -name \\*.zip -exec rm  \\{\\} \\;"); *\/ */
				/* /\* 	      system(command); *\/ */

				/* 	      sprintf(command,"find . -name \\*.CSV -exec ../../fixextension \\{\\} \\;"); */
				/* 	      system(command); */

				/* 	      sprintf(command,"gzip *.[Cc][Ss][Vv]"); */
				/* 	      system(command); */

		      	chdir("../..");
			}
		}
    }
}


/** 
	Allow passing in command line args for start and end years.
	Gain Capital still maintains these data dumps through 05/2017.
	http://ratedata.gaincapital.com/
**/
void parse_cmd(int argc, char* argv[], int *start, int *end)
{
	printf("here");
	switch(argc)
	{
		case 0:
		case 1:
			(*start) = 2009;
			(*end) = 2009;
			break;
		case 2:
			(*start) = atoi(argv[1]);
			(*end) = start;
			break;
		case 3:
			printf("here");
			(*start) = atoi(argv[1]);
			(*end) = atoi(argv[2]);
			break;
		default:
			printf("Invalid parameters, using defaults...\n");
			printf("Usage: getit start_year=2009 end_year=2009\n\n");
			(*start) = 2009;
			(*end) = 2009;
			break;
	}
}


