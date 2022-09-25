#include <iostream>
#include <string>
#include <fstream>
#include <set>
#include <vector>
#include <cstring>
using namespace std;

struct stream_info {
	uint64_t end_pc, target_pc, inst_cnt;
};

vector<struct stream_info> cpt_stream;

#define MAXN 20

/*
 * Output: 
 * 1. How many loops (stream occurs more than once)
 * 2. How many instructions are in loops with more than N iteration
 */
int total_loop_count = 0;
int total_inst_count = 0;
int inst_iterate_more_than[MAXN];
int loop_iterate_more_than[MAXN];
void loop_count_in_all(int n) {
	// a loop is identified if stream occurs more than once
	// instruction count in loops that iterate more than n times
	memset(inst_iterate_more_than, 0, sizeof(inst_iterate_more_than));
	memset(loop_iterate_more_than, 0, sizeof(loop_iterate_more_than));
	int iterated = 1;
	int cpt_stream_size = cpt_stream.size();
	struct stream_info prev;
	prev.end_pc = 0;
	prev.target_pc = 0;
	prev.inst_cnt = 0;
	for (int i = 0; i < cpt_stream_size; i++) {
		total_inst_count += cpt_stream[i].inst_cnt;
		if (cpt_stream[i].end_pc == prev.end_pc && cpt_stream[i].target_pc == prev.target_pc) {
			// a loop is detected
			if (iterated == 1) {
				++total_loop_count;
			}
			++iterated;
			for (int j = 2; j < MAXN; j++) {
				if (iterated >= j) {
					inst_iterate_more_than[j] += cpt_stream[i].inst_cnt;
				}
			}
		} else {
			// not a loop, update prev
			if (iterated > 1) {
				// we are in a loop, update loop_iterate_more_than
				for (int j = 2; j < MAXN && j < iterated; j++) {
					loop_iterate_more_than[j] += 1;
				}
			}
			prev = cpt_stream[i];
			iterated = 1;
		}
	}

	cout<<"Total inst count = "<<total_inst_count<<", total loop count = "<<total_loop_count<<"\n";
	for (int i = 2; i < MAXN; i++) {
		cout<<"inst count in loops with more than "<<i<<" iterations = "<<inst_iterate_more_than[i]<<"\n";
	}
	for (int i = 2; i < MAXN; i++) {
		cout<<"loop count in loops with more than "<<i<<" iterations = "<<loop_iterate_more_than[i]<<"\n";
	}
	return ;
}
/*
 * Output:
 * How many loops will continue after N iterations
 */
void loop_count_more_than(int n) {
	return ;
}

void loop_possibility_after(int n) {
	return ;
}

int total_partial_count;
int partial_iterate_more_than[MAXN];
void loop_internal_jump_back() {
	int cpt_stream_size = cpt_stream.size();
	struct stream_info prev;
	prev.end_pc = 0;
	int iterated = 1;
        prev.target_pc = 0;
        prev.inst_cnt = 0;
	for (int i = 0; i < cpt_stream_size; i++) {
		if (cpt_stream[i].target_pc == prev.target_pc) {
			// only target pc is required
			if (iterated == 1) {
				++total_partial_count;
			}
			++iterated;
		} else {
			if (iterated > 1) {
                                // we are in a loop, update loop_iterate_more_than
                                for (int j = 2; j < MAXN && j < iterated; j++) {
                                        partial_iterate_more_than[j] += 1;
                                }
                        }
                        prev = cpt_stream[i];
                        iterated = 1;
		}
	}
	for (int i = 2; i < MAXN; i++) {
		cout<<"loop count in partial loops with more than "<<i<<" iterations = "<<partial_iterate_more_than[i]<<"\n";
	}
	return ;
}



int main(int argc, char *argv[]) {
	if (argc != 2) {
		cout<<"No log file path specified!\n";
		return -1;
	}
	FILE *in_file;
	in_file = fopen(argv[1], "r");
	struct stream_info a;

	while (!feof(in_file)) {
		if (fscanf(in_file, "%llx %llx %lld", &a.end_pc, &a.target_pc, &a.inst_cnt) == 3)
			cpt_stream.push_back(a);
		else
			break;
	}
	cpt_stream.push_back((struct stream_info){0,0,0});
	
	loop_count_in_all(MAXN);	
	loop_internal_jump_back();	
	return 0;
}
