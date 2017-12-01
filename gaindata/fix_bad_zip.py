import sys
import zipfile
import os

zfile = sys.argv[1]
mvfile = zfile[:-3] + "csv"


unzipPath = os.path.dirname(zfile) + '/'
zip_ref = zipfile.ZipFile(zfile, 'r')
zip_ref.extractall(unzipPath)
zip_ref.close()

directory = "."
for root,dirs,files in os.walk(directory):
	for file in files:	
		if file.endswith(".csv") and zfile[-17:-10] in file:
			zip_ref = zipfile.ZipFile(zfile, 'w')	
			print("Moving extracted file '" + root + '/' + file + "' to '" + mvfile + "'...") 
			os.rename(root + '/' + file, mvfile)	
			zip_ref.write(mvfile)
			print("Created zip file.")
			os.remove(mvfile)

zip_ref.close()
