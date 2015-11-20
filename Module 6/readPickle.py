import pickle

file = open("BadMoves", 'rb')
data = pickle.load(file)
file.close()

for line in data:
    if max(line[0]) == line[0][0]:
        element = 2048
    elif max(line[0]) == line[0][3]:
        element = 1536
    elif max(line[0]) == line[0][15]:
        element = 1024
    elif max(line[0]) == line[0][11]:
        element = 512
    else:
        element = 0
    if len(line[0]) > 16:
        line[0][16] = element
    else:
        line[0].append(element)

new_file = open("ExtraInfoBadMoves", "wb")
pickle.dump(data, new_file, protocol=pickle.HIGHEST_PROTOCOL)
new_file.close()

print("Len:", len(data))
