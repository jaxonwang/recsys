import sys

class DataCounter:


	movie_rating = []
	movie_rating_data = []

	def movieRatedByUser(self):
		pass

	def dataReader(self, data_file_path):
		with open(data_file_path) as data_file:
			count = 0
			for line in data_file:
				line = line.strip().split("::")
				record = [int(line[0]),int(line[1]),float(line[2]),int(line[3])] 
				self.movie_rating_data.append(tuple(record))
				count += 1
				
	def print_all(self):
		for i in self.movie_rating_data:
			print i

if __name__ == "__main__":
	datacounter = DataCounter()
	datacounter.dataReader("..//MovieLensDS//ratings.dat")
	print "read done."
	#datacounter.print_all()

