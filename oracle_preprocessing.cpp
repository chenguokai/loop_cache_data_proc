#include <iostream>
#include <cstdio>
#include <string>
#include <set>
using namespace std;

struct trace{
	uint64_t pc;
	int taken;
	int type;
	uint64_t target;

	bool operator < (const struct trace a) const {
		return pc < a.pc || (pc == a.pc && taken < a.taken) ||
		(pc == a.pc && taken == a.taken && type < a.type) ||
		(pc == a.pc && taken == a.taken && type == a.type && target < a.target);
	}
} mytrace;

struct trace_taken{
	uint64_t pc;
	int type;
	uint64_t target;

	struct trace_taken operator =(struct trace a) {
		pc = a.pc;
		type = a.type;
		target = a.target;
		return *this;
	}
	bool operator < (const struct trace_taken a) const {
                return pc < a.pc ||
                (pc == a.pc && type < a.type) ||
                (pc == a.pc && type == a.type && target < a.target);
        }
} mytaken;

set<struct trace_taken> s;

int main(int argc, char *argv[]) {
	if (argc != 2) {
		printf("not enough arguments, proc [FILE]\n");
	}
	FILE *fp, *res;
	fp = fopen(argv[1], "r");
	string str = argv[1]; //  + "_processed"
	str += "_processed";
	res = fopen(str.c_str(), "w");
	while (fscanf(fp, "%llx,%d,%d,%llx", &mytrace.pc, &mytrace.taken, &mytrace.type, &mytrace.target) != EOF) {
		mytaken = mytrace;
		if (!mytrace.taken && s.find(mytaken) == s.end()) {
			// do not print
			printf("Ignored never taken branch at %llx\n", mytrace.pc);
		} else {
			fprintf(res, "%llx,%d,%d,%llx\n", mytrace.pc, mytrace.taken, mytrace.type, mytrace.target);
		}
		// if taken, add to history
		if (mytrace.taken) {
			s.insert(mytaken);
		}
	}
	return 0;
}
