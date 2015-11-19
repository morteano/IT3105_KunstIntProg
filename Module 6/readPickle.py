import pickle

file = open("PickleMoves", 'rb')
data = pickle.load(file)
file.close()

for line in data:
    if max(line[0]) == line[0][0]:
        line[0].append(1)
    elif max(line[0]) == line[0][3]:
        line[0].append(2)
    elif max(line[0]) == line[0][15]:
        line[0].append(3)
    elif max(line[0]) == line[0][11]:
        line[0].append(4)
    else:
        line[0].append(0)

new_file = open("ExtraInfo", "wb")
pickle.dump(data, new_file, protocol=pickle.HIGHEST_PROTOCOL)
new_file.close()

print("Len:", len(data))
