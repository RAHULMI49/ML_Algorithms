import json
import os
import cPickle as pickle

def dump(filename, data):
	with open(filename, 'w') as f:
		json.dump(data, f)
	print ('filename %s created \n' %(filename))

def load_json_data(filename):
	with open(filename, 'r') as f:
		data = json.load(f)
	return data

def pickle_dump(object_, filename):
	pickle.dump(object_, open(filename, 'wb'))

def pickle_load(filename):
	data = pickle.load(open(filename, 'rb'))
	return data

def dump_into_txt(filename, data_string):
	text_file = open(filename, "w")
	text_file.write(data_string)
	text_file.close()
	print ('filename %s created \n' %(filename))


def get_h_m_s(seconds):
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	return "%s : %s : %s "%(h, m, s)


def calculate_ETC(time_passed, units_processed, units_remaining):
	return time_passed * (units_remaining / float(units_processed))

def clear_dir(directory):
	for f in os.listdir(directory): os.remove(directory + '/' + f)

def remove_non_ascii(text):
	text = ''.join([i if ord(i) < 128 else ' ' for i in text]).strip()
	return text