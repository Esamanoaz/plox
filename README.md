# Plox - a python interpreter for the Lox programming language

## Description
This is my interpreter implementation of Lox in Python 3. I heavily borrowed this from [JHonaker's Pylox](https://github.com/JHonaker/pylox) to start. Checkout the online book [Crafting Interpreters](http://craftinginterpreters.com/) for free to learn about interpreters, compilers, and how to write them.

## Why Python?
In the first section of the book, Bob Nystrom writes his interpreter for Lox in Java. I chose to write mine in Python because I am comfortable with it, and it required me to think a bit more about what code I was writing instead of just `ctrl c`'ing and `ctrl v`'ing Java code (although I did read through JHonaker's scanner quite a few times).

## Significant differences from my plox and Nystrom's jlox
* C-style multiline comments (`/* comments */`).
