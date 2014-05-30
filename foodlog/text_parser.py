# -*- coding: utf-8 -*-
"""
"""

from decimal import Decimal
from pprint import pprint

from pyparsing import *

ws = ' \t'
ParserElement.setDefaultWhitespaceChars(ws)

# Define punctuation and legal characters.
backslash = '\\'
hashmark = '#'
colon = ':'

unicode_printables = ''.join(chr(c) for c in range(65536)
                             if not chr(c).isspace())

standard_chars = unicode_printables.replace(backslash, '').replace(hashmark, '')
key_chars = unicode_printables.replace(colon, '')



# Escape codes.
escaped_hash = Literal(backslash + hashmark)
escaped_backslash = Literal(backslash + backslash)
# escape = (backslash + Word(printables, exact=1)) | escaped_hash | escaped_backslash
 
# Free-form text includes internal whitespace, but not leading or trailing.
text = OneOrMore(White(ws) | Word(standard_chars))
text.setParseAction(lambda tokens: ''.join(tokens).strip())


# comment = (hashmark + restOfLine).suppress()
 
# Define line-related parts.
EOL = LineEnd().suppress()
SOL = LineStart().leaveWhitespace()
# continuation = (Literal(backslash).leaveWhitespace() + EOL).suppress()
blankline = SOL + LineEnd()

 
header = Suppress(hashmark) + text + EOL

key = OneOrMore(White(ws) | Word(key_chars))
key.setParseAction(lambda tokens: ''.join(tokens))

decimal = Regex(r'\d*[\.\,]?\d+')
decimal.setParseAction(lambda t: Decimal(t[0].replace(r',', r'.')))
unit = oneOf((r'µg', r'mg', r'g', r'l', r'kcal'))

value = decimal + unit
value.setParseAction(tuple)

def hd(tokens):
    pprint(tokens)
    return (tokens[0], tokens[1:])

sub_assignment = Suppress('-') + key + Suppress(colon) + value + EOL
sub_assignment.setParseAction(tuple)
assignment = key + Suppress(colon) + value + EOL + ZeroOrMore(sub_assignment)
assignment.setParseAction(hd)


food = header + Dict(ZeroOrMore(assignment))
food.setParseAction(lambda tokens: (tokens[0], dict(tokens[1:])))

body = Dict(OneOrMore(food))
parser = body + StringEnd()
parser.ignore(blankline)

if __name__ == '__main__':
    try:
        with open(r'E:\data\foods.md', encoding="utf-8") as fp:
            r = parser.parseString(fp.read())
            pprint(dict(r))
    except ParseException as err:
        print(err.line)
        print(" " * (err.column - 1) + "^")
        print(err)

