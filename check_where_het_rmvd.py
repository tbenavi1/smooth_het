import sys
#python check_where_het_rmvd.py file.fasta loc_replacements.txt track2.mode.bed track3.mode.bed track.ue.mode.bed

#track4.bed track5.bed track6.bed track7.bed track8.bed

#Ex.
# python ./check_where_het_rmvd.py het_rmvd_loc_test.txt ~/Desktop/smooth_het/simulation.chr20.gs28100000.cov30.het4.rs10000.random_het1.gc-1.rc.err1.repeats0.noErrRecorded.fasta ~/Downloads/loc_replacements_simulation.gs28100000_cov30_het4_rs10000_random_het1_rc_k21_gc-1_err1_repeats0.txt
# python ./check_where_het_rmvd.py het_rmvd_loc_test.txt ~/Desktop/smooth_het/p_arm_ch20/simulation.chr20.gs28100000.cov30.het1.rs10000.random_het1.gc-1.rc.err1.repeats0.fasta ~/Desktop/smooth_het/loc_replacements_simulation.gs28100000_cov30_het1_rs10000_random_het1_rc_k21_gc-1_err1_repeats0.txt
# python ./check_where_het_rmvd.py het_rmvd_loc_test.txt ~/Desktop/smooth_het/simulation.chr20.gs27981280.cov30.het0.rs10000.random_het1.gc-1.rc.err1.repeats0.fasta ~/Desktop/smooth_het/loc_files/loc_replacements_simulation.gs27981280_cov30_het0_rs10000_random_het1_rc_k21_gc-1_err1_repeats0.txt

#load the genome het locations that are editable by mode (i.e. not too dense)
#make sure pick correct track2.bed file
with open(sys.argv[3], "r") as in_track2:
	track2 = set()
	for line in in_track2:
		loc = int(line.strip().split("\t")[1])
		track2.add(loc)

out_track3 = open(sys.argv[4], "w")
out_track_ue = open(sys.argv[5], "w")
#out_track4 = open(sys.argv[5], "w")
#out_track5 = open(sys.argv[6], "w")
#out_track6 = open(sys.argv[7], "w")
#out_track7 = open(sys.argv[8], "w")
#out_track8 = open(sys.argv[9], "w")

#out = open(sys.argv[1], "w")
#out_all_het = open(sys.argv[2], "w") # bed file with the list of all het sites 
#out_missed_het = open(sys.argv[3], "w") #bed file with the list of the missed 

#read_size = 1000 #assume read_size = 10000

with open(sys.argv[1], "r") as in_fasta, open(sys.argv[2], "r") as in_loc_replacements: #Fasta file and loc_replacements file
	#all_het_spots = []
	#all_err_spots = []
	#starting_spots = []
	#Lines = f.readlines()
	read_name_to_read_track3_het_spots = dict()
	read_name_to_read_track_ue_spots = dict()
	track3_het_spots = set()
	track_ue_spots = set()
	for line in in_fasta:
		if (line.count(">") > 0):
			line1 = line.strip()
			line2 = in_loc_replacements.readline().strip()
			if line2:
				line2 += ","
			read_het_spots=line1.split("|")[4].split(",")[:-1]
			edited_read_het_spots=line2.split(",")[:-1]
			read_name = line1.split("|")[0]
			read_start = int(line1.split("|")[1])
			rc = line1.split("|")[3]
			if rc == "original":
				genome_het_spots = set(read_start + int(x) for x in read_het_spots)
				edited_genome_het_spots = set(read_start + int(x) for x in edited_read_het_spots)
			else:
				read_size = len(in_fasta.readline().strip()) #added as temporary fix
				genome_het_spots = set(read_start + read_size - 1 - int(x) for x in read_het_spots)
				edited_genome_het_spots = set(read_start + read_size - 1 - int(x) for x in edited_read_het_spots)
			#print(set(track2))
			#test = set(genome_het_spots) - set(edited_genome_het_spots)
			#if test:
			#	print(test)
			read_track3_het_spots = (genome_het_spots - edited_genome_het_spots) & track2
			read_track_ue_spots = edited_genome_het_spots - track2
			if read_track_ue_spots:
				read_name_to_read_track_ue_spots[read_name] = read_track_ue_spots
			if read_track3_het_spots:
				read_name_to_read_track3_het_spots[read_name] = read_track3_het_spots
			track_ue_spots |= read_track_ue_spots
			track3_het_spots |= read_track3_het_spots
			#all_het_spots.append(het_spots)
			#err_spots=line1.split("|")[5].split(",")
			#starting_spots.append(int(line.split("|")[1]))
			#for ele in het_spots:
			#	if ele != "":
			#		out_all_het.write("chr_20\t" + str(int(line.split("|")[1]) + int(ele)) + "\t" + str(int(line.split("|")[1]) + int(ele) + 1) + "\n")
			#all_err_spots.append(err_spots)
print(read_name_to_read_track3_het_spots)
print(read_name_to_read_track_ue_spots)
for track3_het_spot in sorted(list(track3_het_spots)):
	out_track3.write(f"chr20\t{track3_het_spot}\t{track3_het_spot+1}\n")
out_track3.close()
for track_ue_spot in sorted(list(track_ue_spots)):
	out_track_ue.write(f"chr20\t{track_ue_spot}\t{track_ue_spot+1}\n")
out_track_ue.close()

#with open(sys.argv[2]) as f_loc_replacements:
#	i = 0
#	Lines = f.readlines()
#	for line in Lines:
#		line = line.strip()
#		rmvd_het = line.split(",")
#		if rmvd_het[0] == '':
#			union_het = 0
#		else:
#			union_het = len(set(rmvd_het) & set(all_het_spots[i]))
#			all_het_union = set(rmvd_het) & set(all_het_spots[i])
#			missed_het = set(all_het_spots[i]).difference(rmvd_het)
#			for each in all_het_union:
#				out.write("chr_20\t" + str(starting_spots[i]+int(each)) + "\t" + str(starting_spots[i]+int(each) + 1) + "\n")
#			for each in missed_het:
#				if each != '':
#					out_missed_het.write("chr_20\t" + str(starting_spots[i]+int(each)) + "\t" + str(starting_spots[i]+int(each) + 1) + "\n")
#		union_err = len(set(rmvd_het) & set(all_err_spots[i]))
#		missed_het = len(all_het_spots[i]) - union_het
#		false_rmvd = len(rmvd_het) - union_het
#		if all_het_spots[i] == '':
#			length_het_spots = 0
#		else:
#			length_het_spots = len(all_het_spots[i])
#		print("read_" + str(i) + "\t" + str(union_het/length_het_spots*100) + "\t" + str(union_err))
#		i = i + 1

#out_missed_het.close()
#out_all_het.close()
#out.close()
