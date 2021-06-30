import spacy


a = open("a.txt","r")
a = {"Brian E Carpenter",
"Choose Account",
"Brian Carpenter"}
nlp = spacy.load("en_core_web_sm")

doc = nlp(x)

for y in doc.ents:
    print(y.label_)

print(type(a))
