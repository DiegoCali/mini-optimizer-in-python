import sys
from myparser import parser

with open("code.tac", "w", encoding="utf-8") as file:
    sys.stdout = file

    parser.parse("""
    score = 72;
    bonus = 8;
    attempts = 3;

    if (score >= 90 || bonus >= 10 || attempts == 3) {
        result = score + bonus;
        print result;
    } else {
        result = score - bonus;
        print result;
    }

    while (attempts > 0) {
        attempts = attempts - 1;
        if (attempts == 1 || score > 70) {
            print score;
        }
    }

    if (score > 100 || bonus > 100 || attempts == 0) {
        print true;
    }
    """)