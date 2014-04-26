import os


def test(keywords,total_pages):
	match = 0

	path = 'downloads'
	
	for filename in os.listdir(path):
		if '.html'in filename:
			download_file = open(os.path.join(path,filename),'r')
			content = download_file.read()

			check = True
			for keyword in keywords.split():
				if keyword not in content:
					check = False
			if check:
				match+=1					
	return match*1.0/total_pages

