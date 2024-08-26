import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def process(user_input):   
     #Tokenizes the sentence 
     post_tokens = word_tokenize(user_input) 
     
     #does pos tag on it for named entity recognition
     post_word = nltk.pos_tag(post_tokens)
     
     if len(post_word) == 1:
          for i in post_word:
               return i[0]
     else:
     #detects the name in the sentences
          detected_names_nltk = [name.title() for name, pos in post_word if pos == 'NNP' or pos == 'JJ' or pos == 'ADJ']
          return detected_names_nltk

def tokenise_word(user_input):
     text_token  = word_tokenize(user_input) #input tokenized
     tokens_without_sw = [word.lower() for word in text_token if not word in stopwords.words('english') and word.isalpha()]
     filtered_sentence = (" ").join(tokens_without_sw)
     return filtered_sentence