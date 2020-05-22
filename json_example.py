'''
		Author: Maanas Talwar
		Purpose:

'''
import json

if __name__ == '__main__':
	print('*****  Start Execution  *****')

	a_dict = {"abc": "def"}

	with open('postgresql.json') as f:
		data = json.load(f)

	print(data)
	print(type(data))
	data['urls'].update(a_dict)

	with open("postgresql.json", 'w+') as f:
		json.dump(data, f, indent = 4)

	# print(json_object['urls']['download'])
	# print(type(json_object))
	print('*****  End Execution  *****')
