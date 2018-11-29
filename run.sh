#!/bin/sh

workon trello-todo
jupyter nbconvert --execute --to html Trello\ Metrics.ipynb

