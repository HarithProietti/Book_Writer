### We generate the events occurring within each chapter (most detailed level)

from utils import BaseEventChain
from langchain_openai import ChatOpenAI

class ChapterPlotChain(BaseEventChain):

    PROMPT = """
    You are a writer and your job is to generate the plot for one and only one chapter of a novel.
    You are provided with information like the title, the main plot, and the main character.
    Also, importantly, I will give you the plots of all previous chapters that have already been written.
    Your plot should accurately describe the story of the chapter, going into details of the main action.
    Make sure the plot you write is consistent with the previous chapters, as well as the main plot that I will provide.

    Also, make sure the summary/plot you write is consistent with the genre of the novel and an author's style I will give you.

    Take into account the following 5 features to write an exciting plot:
    {features}

    Subject: {subject}
    Genre: {genre}
    Author's style: {author}
    Title: {title}
    Main character's profile: {profile}

    Novel's full plot: {plot}

    Outline:
    {outline}

    Chapter plots:
    {summaries}

    Current chapter plot for {chapter}:
    """

    FEATURE_GENERATOR_PROMPT = """
    Generate a list of 5 attributes that characterize an exciting story.

    List of attributes:
    """

    def run(self, subject, genre, author, profile, title, plot, summaries_dict, chapter_dict, chapter):
        
        features = ChatOpenAI().predict(self.FEATURE_GENERATOR_PROMPT)

        outline = '\n'.join(['{} - {}'.format(chapter, description) for chapter, description in chapter_dict.items()])

        summaries = '\n\n'.join(['Plot of {}: {}'.format(chapter, summary) for chapter, summary in summaries_dict.items()])

        plot = self.chain.predict(
            features=features,
            subject=subject,
            genre=genre,
            author=author,
            profile=profile,
            title=title,
            plot=plot,
            outline=outline,
            summaries=summaries,
            chapter=chapter
        )

        return plot


# this chain creates the list of events for each chapter
class EventsChain(BaseEventChain):

    PROMPT = """
    Your job is to come up with a detailed list of events happening in the current chapter of a novel.
    Those events describe the plot of the chapter and the actions of the different characters.
    I will give you the title of the novel, the main plot of the novel, the main character, and a summary of the current chapter.
    Additionally, I will give you the list of events that happened in the previous chapters.
    The list of events should be consistent with the genre of the novel, as well as the author's style.
    Each element of the list of events should be returned on a single line, as indicated by the following template:

    [Content of Event 1]
    [Content of Event 2]
    ...
    [Content of Event N]

    Example of possible output for 3 events within a chapter: 

    John goes within the forest and meets a man named Henry.
    Henry is shy and initially doesn't want to talk to John, but after a few minutes he starts opening.
    A few hours later, they're like best friends, and decide to go back to the savanna together.

    Here is the additional information:
    Subject: {subject}
    Genre: {genre}
    Author's style: {author}

    Title: {title}
    Main character: {profile}

    Novel's plot: {plot}

    Events from previous chapters: {previous_events}

    Summary of the current chapter:
    {summary}

    Please only return the events.
    Event list:
    """

    def run(self, subject, genre, author, profile, title, plot, summary, event_dict, chapter):
    
        previous_events = ''
        for chapter, events in event_dict.items():
            previous_events += '\n' + chapter
            for event in events:
                previous_events += '\n' + event

        response = self.chain.predict(
            subject=subject,
            genre=genre,
            author=author,
            profile=profile,
            title=title,
            plot=plot,
            summary=summary,
            previous_events=previous_events
        )

        return self.parse(response)
    
    def parse(self, response):
        event_list = response.strip().split('\n')
        event_list = [event.strip() for event in event_list if event.strip()]
        return event_list
    

def get_events(subject, genre, author, profile, title, plot, chapter_dict):
    chapter_plot_chain = ChapterPlotChain()
    events_chain = EventsChain()
    summaries_dict = {}
    event_dict = {}

    for chapter, _ in chapter_dict.items():

        summaries_dict[chapter] = chapter_plot_chain.run(
            subject, genre, author, profile, title, plot, summaries_dict, chapter_dict, chapter
        )
        
        event_dict[chapter] = events_chain.run(
            subject, genre, author, profile, title, plot, summaries_dict[chapter], event_dict, chapter
        )
    
    return summaries_dict, event_dict