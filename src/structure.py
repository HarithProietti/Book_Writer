### Title, plot, chapter list
from utils import BaseStructureChain, ChatOpenAI

class TitleChain(BaseStructureChain):

    # We override the empty prompt variable
    PROMPT = """
    Your job is to generate the title for a novel about the following subject and main character.
    Only return a title!
    The title should be consistent with a genre and author's style that will be mentioned.

    Subject: {subject}
    Genre: {genre}
    Author's style: {author}

    Main character's profile: {profile}

    Title:
    """

    def run(self, subject, genre, author, profile):
        return self.chain.predict(
            subject=subject,
            genre=genre,
            author=author,
            profile=profile
        )
    
class PlotChain(BaseStructureChain):

    PROMPT = """
    Your task is to generate a plot for a novel.
    The plot should describe the characters involved (you should create some characters, be inventive!) and the main events the happen during the novel. Please be explicit about the character's names and how they interact.
    To help you, you will be provided a subject, a title and the main character's profile.
    You will also be provided with the genre of the novel, and a famous author's style.
    Make sure the main character is actually at the center of the novel.
    Please only return a plot.

    Considering the following attributes:

    5 features the novel should have: {features}

    Subject: {subject}
    Genre: {genre}
    Author's style: {author}
    Title: {title}
    Main character's profile: {profile}

    Plot:
    """

    FEATURE_GENERATOR_PROMPT = """
    Generate a list of 5 attributes that characterize an exciting story.

    List of attributes:
    """

    def run(self, subject, genre, author, profile, title):
        features = ChatOpenAI().predict(self.FEATURE_GENERATOR_PROMPT)

        plot = self.chain.predict(
            features=features,
            subject=subject,
            genre=genre,
            author=author,
            profile=profile,
            title=title
        )

        return plot
    
class ChaptersChain(BaseStructureChain):

    PROMPT = """
    Your job is to generate a list of chapters of a novel, based on a title, a plot and a main character that I will provide.
    Generate a list of chapters describing the plot of the novel.
    Make sure that the chapters are consistent with the plot, as well as the genre of the novel, and an famous author's style.

    Please follow this template:

    Prologue: [description of prologue]
    Chapter 1: [description of chapter 1]
    ...
    Epilogue: [description of epilogue]

    So as you have noticed, each line is composed of the chapter number followed by a commma, and a description.

    Subject: {subject}
    Genre: {genre}
    Author's style: {author}

    Title: {title}
    Main character's profile: {profile}

    Plot: {plot}

    Only return a chapter list following the template mentioned before.
    Chapters' list:
    """

    def run(self, subject, genre, author, profile, title, plot):
        response = self.chain.predict(
            subject=subject,
            genre=genre,
            author=author,
            profile=profile,
            title=title,
            plot=plot
        )

        return self.parse(response)
    
    def parse(self, response):
        # parses the chapters list provided by the llm
        chapter_list = response.strip().split('\n')
        chapter_list = [chapter for chapter in chapter_list if ':' in chapter]
        chapter_dict = dict([chapter.strip().split(':') for chapter in chapter_list])

        return chapter_dict

def get_structure(subject, genre, author, profile):
    # main function that calls the different classes
    title_chain = TitleChain()
    plot_chain = PlotChain()
    chapters_chain = ChaptersChain()

    title = title_chain.run(
    subject=subject,
    author=author,
    genre=genre,
    profile=profile
    )
# ex of good one generated: The Lion's Rebellion: A Tale of Nature's War

    plot = plot_chain.run(
        subject=subject,
        author=author,
        genre=genre,
        profile=profile,
        title=title
    )

    chapters_dict = chapters_chain.run(
        subject=subject,
        author=author,
        genre=genre,
        profile=profile,
        title=title,
        plot=plot
    )

    return title, plot, chapters_dict