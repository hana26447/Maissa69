from token import Tokeniser, get_doc, get_requet
from filtrage import filter 

requet = get_requet("requet.txt")

doc = get_doc()
tokens = Tokeniser(requet)
stoplist =['the', 'of', 'in', 'on', 'to', 'a', 'has', 'been', 'most', 'around', 'due', 'are', 'that', 'can', 'lot']

tok =[[t for t in sublist if t not in stoplist] for sublist in tokens]


print(requet)