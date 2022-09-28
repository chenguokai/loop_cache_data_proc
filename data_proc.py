import os

rootdir = '/nfs/home/chenguokai/loop_perf/take_cpt/'

point_set = set()

total_weight = dict()
total_inst_cnt = dict()
total_loop_cnt = dict()

# list for 0 ... MAXN - 1
inst_cnt_in_loops_more_than_N = [dict() for x in range(20)]
loop_stream_size = [dict() for x in range(20)]
early_end_inst_cnt_in_loops_more_than_N = [dict() for x in range(20)]
early_end_loop_cnt_in_loops_more_than_N = [dict() for x in range(20)]
partial_loop2_inst_cnt_in_loops_more_than_N = [dict() for x in range(20)]
partial_loop3_inst_cnt_in_loops_more_than_N = [dict() for x in range(20)]
partial_loop2_loop_cnt_in_loops_more_than_N = [dict() for x in range(20)]
partial_loop3_loop_cnt_in_loops_more_than_N = [dict() for x in range(20)]

for point in os.listdir(rootdir):
	splited = point.rsplit('_', 2)
	#print(splited)
	file_path = rootdir + '/' + point + '/0/'
	# find txt file
	txt_path = ""
	for filenm in os.listdir(file_path):
		if filenm.endswith('.txt'):
			txt_path = file_path + filenm
	
	local_weight = float(splited[2])
	
	lines = []
	with open(txt_path) as txt_file:
		lines = txt_file.readlines()
		
	if not splited[0] in point_set:
		# not inited, add to total_weight
		total_weight[splited[0]] = 0.0
		total_inst_cnt[splited[0]] = 0.0
		total_loop_cnt[splited[0]] = 0.0
		for i in range(20):
			inst_cnt_in_loops_more_than_N[i][splited[0]] = 0.0
			loop_stream_size[i][splited[0]] = 0.0
			early_end_inst_cnt_in_loops_more_than_N[i][splited[0]] = 0.0
			early_end_loop_cnt_in_loops_more_than_N[i][splited[0]] = 0.0
			partial_loop2_inst_cnt_in_loops_more_than_N[i][splited[0]] = 0.0
			partial_loop3_inst_cnt_in_loops_more_than_N[i][splited[0]] = 0.0
			partial_loop2_loop_cnt_in_loops_more_than_N[i][splited[0]] = 0.0
			partial_loop3_loop_cnt_in_loops_more_than_N[i][splited[0]] = 0.0
	
	orig = total_weight[splited[0]] + local_weight
	total_weight.update({splited[0]:orig})
	
	for cur_line in lines:
		line_split = cur_line.split(' ')
		if line_split[0] == 'Total' and line_split[1] == 'inst':
			total_inst_cnt.update({splited[0]:(total_inst_cnt[splited[0]] + local_weight * float(line_split[-1]))})
		elif line_split[0] == 'total' and line_split[1] == 'loop':
			total_loop_cnt.update({splited[0]:(total_loop_cnt[splited[0]] + local_weight * float(line_split[-1]))})
		elif line_split[0] == 'inst' and line_split[1] == 'count' and line_split[3] == 'loops':
			inst_cnt_in_loops_more_than_N[int(line_split[7])].update({splited[0]:inst_cnt_in_loops_more_than_N[int(line_split[7])][splited[0]] + local_weight * float(line_split[-1])})
		elif line_split[0] == 'loop' and line_split[1] == 'stream':
			loop_stream_size[int(line_split[3])].update({splited[0]:loop_stream_size[int(line_split[3])][splited[0]] + local_weight * float(line_split[-1])})
		elif line_split[0] == 'loop' and line_split[1] == 'count' and line_split[3] == 'early':
			early_end_loop_cnt_in_loops_more_than_N[int(line_split[-4])].update({splited[0]:early_end_loop_cnt_in_loops_more_than_N[int(line_split[-4])][splited[0]] + local_weight * float(line_split[-1])})
		elif line_split[0] == 'loop' and line_split[1] == 'count' and line_split[3] == 'partial' and line_split[5] == '2':
			partial_loop2_loop_cnt_in_loops_more_than_N[int(line_split[-4])].update({splited[0]:partial_loop2_loop_cnt_in_loops_more_than_N[int(line_split[-4])][splited[0]] + local_weight * float(line_split[-1])})
		elif line_split[0] == 'partial' and line_split[1] == 'loop' and line_split[2] == '2':
			partial_loop2_inst_cnt_in_loops_more_than_N[int(line_split[-3])].update({splited[0]:partial_loop2_inst_cnt_in_loops_more_than_N[int(line_split[-3])][splited[0]] + local_weight * float(line_split[-1])})
		elif line_split[0] == 'loop' and line_split[1] == 'count' and line_split[3] == 'partial' and line_split[5] == '3':
			partial_loop3_loop_cnt_in_loops_more_than_N[int(line_split[-4])].update({splited[0]:partial_loop3_loop_cnt_in_loops_more_than_N[int(line_split[-4])][splited[0]] + local_weight * float(line_split[-1])})		
		elif line_split[0] == 'partial' and line_split[1] == 'loop' and line_split[2] == '3':
			 partial_loop3_inst_cnt_in_loops_more_than_N[int(line_split[-3])].update({splited[0]:partial_loop3_inst_cnt_in_loops_more_than_N[int(line_split[-3])][splited[0]] + local_weight * float(line_split[-1])})

	# record as a point
	point_set.add(splited[0])

print(total_weight)
#print(inst_cnt_in_loops_more_than_N[2]['bwaves'])
print("inst in loops more than 2")
print(inst_cnt_in_loops_more_than_N[2])
print()
print()
#print(loop_stream_size[4]['bwaves'])
print(loop_stream_size)
#print(early_end_loop_cnt_in_loops_more_than_N[2]['bwaves'])
print(early_end_loop_cnt_in_loops_more_than_N)
#print(partial_loop2_inst_cnt_in_loops_more_than_N[2]['bwaves'])
print(partial_loop2_inst_cnt_in_loops_more_than_N)
#print(partial_loop3_inst_cnt_in_loops_more_than_N[2]['bwaves'])
print(partial_loop3_inst_cnt_in_loops_more_than_N)
#print(partial_loop2_loop_cnt_in_loops_more_than_N[2]['bwaves'])
print(partial_loop2_loop_cnt_in_loops_more_than_N)
#print(partial_loop3_loop_cnt_in_loops_more_than_N[2]['bwaves'])
print(partial_loop3_loop_cnt_in_loops_more_than_N)
