VPATH = /nfs/home/chenguokai/loop_perf/take_cpt
PROC = /nfs/home/chenguokai/loop_perf/data_proc/proc
LOGS := ${wildcard ${VPATH}/*/0/*.log}
OBJECTS := $(patsubst %.log, %.txt, ${LOGS})


all: ${OBJECTS}

%.txt: %.log
	${PROC} $< > $@

clean:
	rm ${OBJECTS}
