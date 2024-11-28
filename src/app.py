from dotenv import load_dotenv
load_dotenv()

from characters import MainCharacterChain
from structure import get_structure
from events import ChapterPlotChain, EventsChain, get_events

subject = 'War between the forest and the savanna'
author = 'William Shakespeare'
genre = 'Sci-Fi'

main_character_chain = MainCharacterChain()
profile = main_character_chain.run('Kevin_Richardson_(zookeeper).pdf')

title, plot, chapter_dict = get_structure(subject, genre, author, profile)
summaries_dict, event_dict = get_events(subject, genre, author, profile, title, plot, chapter_dict)

# print(title)
# print(plot)
# print(chapter_dict)
# print('chapter dict', chapter_dict)
# for chapter, plot in summaries_dict.items():
#     print(chapter)
#     print(plot)
#     print()
for chapter, events in event_dict.items():
    print(chapter)
    print(events)
    print()