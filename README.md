# Book_Writer

To define a book, several key points to define:

- Subject
- Genre
- Possibly, an author's style
- Main character's description: to add more interesting context (and challenge!), I've chosen the wikipedia file of a well-known zoologist ('The Lion whisperer'), which we'll process with langchain.

Once these arguments are defined, we generate (with the LLM) a title, and a plot.

The plot should be split as a classical book structure, starting with a Prologe, Chapters, Epilogue...

For each chapter, we will generate the corresponding information:

Chapter Name --> Chapter Plot --> List of events --> List of paragraphs per event

The final book will then be defined as the list of paragraphs from all chapters.



## Additional details

python-docx allows to write the final book in a Word format.
