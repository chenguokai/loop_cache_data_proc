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
loop_cache_hit_inst = [dict() for x in range(20)]
loop_cache_hit_loop = [dict() for x in range(20)]


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
			loop_cache_hit_inst[i][splited[0]] = 0.0
			loop_cache_hit_loop[i][splited[0]] = 0.0
				
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
		elif line_split[0] == 'loop' and line_split[1] == 'cache' and line_split[-1] == 'inst\n':
			#print('debug')
			loop_cache_hit_inst[int(line_split[3])].update({splited[0]:loop_cache_hit_inst[int(line_split[3])][splited[0]] + local_weight * float(line_split[-2])})
		elif line_split[0] == 'loop' and line_split[1] == 'cache' and line_split[-1] == 'loop\n':
			loop_cache_hit_loop[int(line_split[3])].update({splited[0]:loop_cache_hit_loop[int(line_split[3])][splited[0]] + local_weight * float(line_split[-2])})
		# print(line_split)
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


import matplotlib.pylab as plt

inst_in_loop_more_than2 = inst_cnt_in_loops_more_than_N[2].items()

x,y = zip(*inst_in_loop_more_than2)

plt.figure(0, figsize=(24,12)) # set figure size
plt.bar(x,y, label='2')
plt.xticks(rotation=-60)    # x axis rotation
#plt.savefig('./inst_in_loop_more_than2iteration.jpg')


inst_in_loop_more_than10 = inst_cnt_in_loops_more_than_N[10].items()
x,y = zip(*inst_in_loop_more_than10)
plt.bar(x,y, label = '10')

inst_in_loop_more_than18 = inst_cnt_in_loops_more_than_N[18].items()
x,y = zip(*inst_in_loop_more_than18)
plt.bar(x,y,label='18')
plt.legend()
plt.savefig('./inst_in_loop_more_than2_10_18iteration.jpg')

plt.figure(1, figsize=(24,12))
plt.xticks(rotation=-60)    # x axis rotation
for i in range(1,8):
	stream_size = loop_stream_size[i].items()
	x,y = zip(*stream_size)
	plt.bar(x,y, label = str(i))

plt.legend()
plt.savefig('./stream_size_2_8.jpg')

plt.figure(2, figsize=(24,12))
plt.xticks(rotation=-60)

for i in [2, 6, 12, 18]:
	partial_2_inst = partial_loop2_inst_cnt_in_loops_more_than_N[i].items()
	x,y = zip(*partial_2_inst)
	plt.bar(x,y, label = str(i))

plt.legend()
plt.savefig('./partial_loop2_inst.jpg')

plt.figure(3, figsize=(24,12))
plt.xticks(rotation=-60)

for i in [2, 6, 12, 18]:
	partial_2_loop = partial_loop2_loop_cnt_in_loops_more_than_N[i].items()
	x,y = zip(*partial_2_loop)
	plt.bar(x,y, label = str(i))

plt.legend()
plt.savefig('./partial_loop2_loop.jpg')

plt.figure(4, figsize=(24,12))
plt.xticks(rotation=-60)

for i in [2, 6, 12, 18]:
	partial_3_inst = partial_loop3_inst_cnt_in_loops_more_than_N[i].items()
	x,y = zip(*partial_3_inst)
	plt.bar(x,y, label = str(i))
plt.legend()
plt.savefig('./partial_loop3_inst.jpg')

plt.figure(5, figsize=(24,12))
plt.xticks(rotation=-60)

for i in [2, 6, 12, 18]:
	partial_3_loop = partial_loop3_loop_cnt_in_loops_more_than_N[i].items()
	x,y = zip(*partial_3_loop)
	plt.bar(x,y, label = str(i))

plt.legend()
plt.savefig('./partial_loop3_loop.jpg')

plt.figure(6, figsize=(24,12))
plt.xticks(rotation=-60)

for i in [7,6,5,4,3,2,1]:
	cache_size_inst = loop_cache_hit_inst[i].items()
	x,y = zip(*cache_size_inst)
	plt.bar(x,y, label = str(i))

plt.legend()
plt.savefig('./loop_cache_inst.jpg')
