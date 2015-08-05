# KanTan

KanTan is a tool designed to make kanji lookup easier by combining kanji lookup and word lookup into one. KanTan allows you to
specify a pattern for a word using the radicals that you recognize, and find all the words that match that pattern.

A live version can be found [here](http://itayperl.github.io/kantan/ui).

### backend/

The backend is a JSON webservice that accepts a search term (i.e. a radical
pattern) and returns a list of matching words. The backend is written in Python 2.

To install all dependencies, run

    pip install -r requirements.txt

Then, to run the webservice:

    python main.py

Example query: `http://localhost:4000/[]顔`

### ui/

The UI is a simple angular app that queries the backend. To use it, run `make`
to compile the CoffeeScript into JS, and just serve the files from the directory.

You may want to edit the location of the backend server in `query_service.coffee`
