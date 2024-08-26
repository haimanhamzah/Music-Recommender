from agent_func import playlist_recommendations
from config import *
from tokenisation import *
from matrixfac import *
from classes import *

"""DISCLAIMER: TO CHANGE THE PLAYLIST ID AND PUT YOUR OWN SONG NAME, HEAD OVER TO CONFIG.PY"""
"""SAME CAN BE SAID FOR ARTISTS SIMILARITIES"""

def main():
    # nltk.download('punkt')
    # nltk.download('averaged_perceptron_tagger')
    # nltk.download('stopwords')
    # nltk.download('wordnet')
    # nltk.download('universal_tagset')
    print("Hi there, What is your name?")
    user_name = input("You: ")
    lemmatized_name = process(user_name)
    lemmatized_name = ''.join(lemmatized_name)

    print("------------------------------------------------------------------------------------------")

    print(f"Hi there, Nice to meet you {lemmatized_name}!, Welcome to the Music Recommender System")

    print("------------------------------------------------------------------------------------------")

    print("Choose among the available options")
    print("------------------------------------------------------------------------------------------")
    print("0 - Get the tracks recommendation based on a song name in a playlist based on content")
    print("1 - Get the artists most similar to your liking based on spotify community")
    print("2 - Scan through a dataset to process Matrix Factorisation based on user likings")
    print("DISCLAIMER: 2 TAKES QUITE A WHILE TO LOAD")
    print("------------------------------------------------------------------------------------------")
    print("Type 'exit' to quit")

    flag = True
    while(flag): 
        user_input = input("You: ")
        if(user_input == "0"):
            input_song_name = "Jasmine"
            recommendations = playlist_recommendations(input_song_name, amount=5)
            print(f"recommended songs based on '{input_song_name}':")
            print(recommendations.to_string(index=False))
        elif(user_input == "1"):
            art = music_df1
            print(art.to_string(index=False))
        elif(user_input == "2"):
            matrix_factorisation()
        elif(user_input == "exit"):
            print("Thank you for using out Music Recommender System! Bye!")
            break
        else:
            print("Sorry please try again")

if __name__ == "__main__":
     main()