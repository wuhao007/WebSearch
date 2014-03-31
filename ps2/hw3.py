word_map = {}

def mainfun():


	# declare some variable to use:
	global word_map
	pos = 0 # the current pos in the current inverted list file
	file_in_used = None
	new_file_count = 0
	start_pos = -1
	size = -1
	word_first_docID = -1
	end_chunk_docID = -1
	lexicon_write_map = {} #this is a map that stores all the info for the line that needs to be written 
	#into the lexicon file
	count_docID_in_chunk = 0
	chunk_size = 10
	new_file_name = None
	at_the_beginning = 0 # indicate whether it is in the beginning, 0 is yes, 1 is not
	fre = 1 # frequency of the word
	fre_list = []
	pre_wordID = ''
	lexicon_map_line = 1




	# open a new inverted list file to write
	new_file_new = new_file_count
	new_file_count += 1 
	new_file_name = 'inverted_list_'+str(new_file_count)
	file_in_used = open(new_file_name,'ab')

	#open the lexicon file:
	lexicon = open("lexicon.map",'ab')


	# actual code below:
	raw_merge_file = open('merge.rpt', 'rb')
	# reading the orignal file, for each line
	for line in raw_merge_file:
		data = line.split()
		word = data[0]
		
		word_DocID = int(data[1])
		if(at_the_beginning == 0):
			print ''
		elif(pre_wordID == word_DocID and pre_word == word):
			fre +=1
			continue
		else:
			fre_list.append(fre)
			fre = 1

		# in the chunk is full, we need to write to the lexicon(end_docID). 
		if(count_docID_in_chunk>chunk_size):
			end_docID_list.append(word_DocID)
			count_docID_in_chunk = 0
			#write the frequncy

			for f in fre_list:
				file_in_used.write(' '+ str(f))

			fre_list = [] 

		count_docID_in_chunk+=1

		# if the word in the word_map, it means that we need to continue writing in the inverted list
		if(word in word_map):
			file_in_used.write(' '+str(word_DocID))
		# if the word is not in the word_map, we need to create new posting for it
		else:
			word_map[word] = lexicon_map_line
			lexicon_map_line+=1
			pos = file_in_used.tell()
			

			if(pos>100000): # if the curent inverted list is too large, we will create another one
				file_in_used.close()
				new_file_new = new_file_count
				new_file_count+=1
				new_file_name = 'inverted_list_'+str(new_file_count)
				file_in_used = open(new_file_name,'ab')
				pos = 0 #set the pos back to 0 since open a new file

			#ok, now it comes a new word.
			if(at_the_beginning == 0):
				print "at the front"
				at_the_beginning =1
				# it means that it is the first postings
			else: # if it is not the first one, we should write all the info and strart a new line
				
				#write the frequncy
				if(end_docID_list!=None):
					end_docID_list.append(pre_wordID)

				if(fre_list==None):
					fre_list.append(1)
				for f in fre_list:
					file_in_used.write(' '+ str(f))
				fre_list = []

				pos = file_in_used.tell()
				size = pos - start_pos
				lexicon_write_map['size'] = size

				lexicon.write(lexicon_write_map['word']+' '+lexicon_write_map['file_name']+ ' '+ str(lexicon_write_map['start_pos'])+' '+str(lexicon_write_map['size'])+' '+str(lexicon_write_map['start_docID']))
			   	for end_docID in lexicon_write_map['end_docID_list']:
					lexicon.write(' '+ str(end_docID)) 
				lexicon.write('\n')


			# we can now begin to record sth, this section is to clean old staff and begin new

			end_docID_list = [] # clean the list

			lexicon_write_map['word'] = word
			lexicon_write_map['file_name'] = new_file_name
			lexicon_write_map['start_docID'] = word_DocID
			start_pos = file_in_used.tell()
			lexicon_write_map['start_pos'] = start_pos
			lexicon_write_map['end_docID_list'] = end_docID_list
			######################################################
			file_in_used.write(' '+str(word_DocID))

		pre_wordID = word_DocID
		pre_word = word

	lexicon.close()
	print word_map






			
mainfun()















































