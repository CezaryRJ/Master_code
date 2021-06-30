from scipy import spatial


def word_vector(inn):
    out = []

    for x in inn:
        out.append(ord(x))

    return out

# https://stackoverflow.com/questions/2460177/edit-distance-in-python
def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]



def parse_name(inn):
    tmp = inn.split(" ")

    out = ""

    for x in tmp[:-1]:


        if x[1] == ".":
            out = out + x
        else:
            out = out + x[0] + "."

    out = out + " " + tmp[-1]

    return out

name1 = "Cezary Jaskula"
name2 = "Cezary R. Jaskula"
name3 = "C. R. Jaskula"

vector1 = word_vector(name1)
vector2 = word_vector(name2)
vector3 = word_vector(name3)

print(vector1)
print(vector2)
print(vector3)




result = levenshteinDistance(parse_name(name2),parse_name(name3))

print(result)

print(parse_name(name1))
print(parse_name(name2))
print(parse_name(name3))
