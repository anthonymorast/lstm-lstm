
#include <data_rec.h>
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char **argv)
{
  FILE *outfile;
  FILE *infile;
  data_rec tick;

  if(argc!=3)
    {
      printf("Usage: %s inputfile outputfile\n",argv[0]);
      exit(1);
    }
  
  if((infile = fopen(argv[1],"r"))==NULL)
    {
      perror(argv[1]);
      exit(1);
    }
  
  if((outfile = fopen(argv[2],"w"))==NULL)
    {
      perror(argv[1]);
      exit(1);
    }
  
  while(fread(&tick,1,sizeof(data_rec),infile)==sizeof(data_rec))
    fprintf(outfile,"%ld %f %f\n",tick.time/1000000,tick.bid,tick.ask);

  fclose(infile);
  fclose(outfile);
  return 0;
}
