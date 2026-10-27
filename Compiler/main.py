from myparser import parser

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