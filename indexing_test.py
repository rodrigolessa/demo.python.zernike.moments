import pickle
import pprint
 

pklFile = open('index.pkl', 'rb')

data1 = pickle.load(pklFile)

print('078Rapidash:')
pprint.pprint(data1['078Rapidash'])

pklFile.close()

# Comparando com o original

#text_file = open("index.cpickle", "r")
#lines = text_file.readlines()
#print(lines)
#print(len(lines))
#text_file.close()

#originalFile = open('index.cpickle', 'rb')
#data2 = pickle.load(originalFile)
#print('Original')
#pprint.pprint(data2['bulbasaur'])
#originalFile.close()