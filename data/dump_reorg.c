
#include <stdlib.h>
#include <stdio.h>
#include <database_format.h>


int printrec(datarec *rec)
{
  printf("serial:%ld time:%ld - %f %f\n",rec->serial,rec->time,rec->ask,rec->bid);
}


int main(int argc, char **argv)
{
  FILE *f ;
  datarec d;


  if(argc != 2)
    {
      printf("Usage: %s <filename>\n",argv[0]);
      return -1;
    }

  if( ( f = fopen(argv[1],"r")) == NULL )
    {
      perror(argv[0]);
      exit(1);
    }

  
  while(fread(&d,sizeof(datarec),1,f)==1)
    printrec(&d);

  fclose(f);

}
