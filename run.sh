#!/bin/sh

# activate trello-todo virtualenv
source /Users/nlarusso/.virtualenvs/trello-todo/bin/activate

jupyter nbconvert --execute --to html Trello\ Dashboard.ipynb
date
