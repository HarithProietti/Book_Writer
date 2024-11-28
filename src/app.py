from dotenv import load_dotenv
load_dotenv()

from characters import MainCharacterChain
from structure import get_structure

subject = 'War between the forest and the savanna'
author = 'William Shakespeare'
genre = 'Sci-Fi'

main_character_chain = MainCharacterChain()
profile = main_character_chain.run('Kevin_Richardson_(zookeeper).pdf')

title, plot, chapter_dict = get_structure(subject, genre, author, profile)

print(title)
print(plot)
print(chapter_dict)