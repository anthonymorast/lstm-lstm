
C_OBJS = getit.o repackit.o mergesort.o convert_time.o plotdata.o
CC_OBJS = findgaps.o tick_file.o dates.o
INCPATH=-I.
CFLAGS=
DEPENDFLAGS=-M

all: getit repackit mergesort convert_time findgaps plotdata

getit: getit.o
	gcc -g -I. -o getit getit.o

repackit: repackit.o
	gcc -g -I. -o repackit repackit.o

mergesort: mergesort.o
	gcc -g -I. -o mergesort mergesort.o

convert_time: convert_time.o
	gcc -g -I. -o convert_time convert_time.o

plotdata: plotdata.o
	gcc -g -I. -o plotdata plotdata.o

findgaps: findgaps.o tick_file.o dates.o
	g++ -g -o findgaps findgaps.o tick_file.o dates.o


.c.o:
	gcc -g -c $(INCPATH) $(CFLAGS) $<

.cc.o:
	g++ -g -c $(INCPATH) $(CFLAGS) $<

.depend:
	rm -f .depend
	gcc $(INCPATH) $(DEPENDFLAGS) $(C_OBJS:.o=.c) > .depend
	g++ $(INCPATH) $(DEPENDFLAGS) $(CC_OBJS:.o=.cc) >> .depend

depend:    .depend

ifeq (.depend,$(wildcard .depend))
include .depend
endif
