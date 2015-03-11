def save_mctal_obj(obj,filepath):
	import cPickle, os

	if filepath.lstrip()[0]!='/':   #assume relative path if first non-white character isn't /
		filepath = os.getcwd()+'/'+filepath 

	### type check
	if isinstance(obj,mctal):
		file_out = open(filepath,'wb') 
		obj.picklepath = filepath
		cPickle.dump(obj,file_out)
		file_out.close()

	print "Saved mctal object with the title '"+obj.title+"'' to: '"+filepath+"'"

