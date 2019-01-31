import csv

# sys.path.insert(0,'/home/rahul/skills-sentence-splitting/misc/skills/new_model/whole_data_processing/')
# from CSV import CsvReader,CsvWriter

class CsvReader:
	
	def __init__(self,filename,cols=False,columns = False):

		self.file = open(filename,'r')
		self.reader = csv.reader(self.file)
		if cols:
			if columns:
				self.cols = columns
				self.reader.next()
			else:
				self.cols = self.reader.next() 
		else:
			self.cols = cols
		self.row = False
		# if not read_full:
		self.next()

	def next(self):
		try:
			if not self.cols:
				self.row = self.reader.next()
			else:
				self.row = dict(zip(self.cols,self.reader.next()))
		except StopIteration:
			self.close()
			self.row = False

	def read(self):
		list_ = []
		for row in self.reader:
			if not self.cols:
				list_.append(list(row))
			else:
		 		list_.append(dict(zip(self.cols,list(row))))
		self.close()
		return list_

	def close(self):
		self.file.close()

class CsvWriter:

	def __init__(self,filename,separator='---',cols = False, mode = 'w'):
		self.file = open(filename, mode)
		self.writer = csv.writer(self.file)
		self.separator = separator

	def convert(self,row):
		if type(row)==dict:
			list_ = []
			for col in cols:
				list_.append(row[col])
			row = list_
		for index,element in enumerate(row):
			if type(element)==list:
				row[index] = (self.separator).join(element)
		return row

	def writerow(self,row):
		row = self.convert(row)
		self.writer.writerow(row)

	def writedata(self,data):
		for row in data:
			row = self.convert(row)
			self.writer.writerow(row)
		self.close()
			
	def close(self):
		self.file.close()




if __name__ == '__main__':
	filename = 'data/undergrad_communities.csv'
	file = CsvReader(filename,cols=True)
	data = file.read()
	cols = file.cols
	file_write = CsvWriter('data/new.csv')
	file_write.writerow(cols)
	file_write.writedata(data)
		

	


