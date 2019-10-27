import re
from itertools import chain
from collections import defaultdict, namedtuple

import pandas as pd
from tqdm import tqdm

Address = namedtuple('Address', ['to', 'kai', 'ku', 'mune', 'chome', 'ban',
                                 'go', 'postal', 'endgo', 'tokens'])

class Postman:
    """
    Converts Japanese address in raw string to structured object.
    """
    to_regex = r'(({})都)'.format('|'.join(['東京']))
    ku_regex = r'#TO# (.*区(佃)?)'
    postal_regex =  r'((〒?[０-９0-9]+([ー－‐-])){1,}([０-９0-9]+))'
    chome_ban_go = r'([0-9０-９一⼀⼆三四五六七⼋九⼗ー]+([{}]+))' # Generic pattern for chome, ban and go.
    chome_regex = chome_ban_go.format('丁目')
    ban_regex = chome_ban_go.format('番街目')
    go_regex = chome_ban_go.format('号棟室館')
    endgo_regex = r'(([0-9０-９一⼀⼆三四五六七⼋九⼗]+$))' # Number at the end.
    ban_go_regex = ban_regex + go_regex + '?' # Not useful?
    mune_regex = r'([0-9０-９Ａ-Ｚ一⼀⼆三四五六七⼋九⼗]+([号]?[棟]))'
    kai_regex = r'(([0-9０-９ー]+|[一⼀⼆三四五六七⼋九⼗]+)[階Ｆ])'

    JAPANESE_ADDRESS_REGEXES = [
        (to_regex, ' #TO# '),
        (kai_regex, ' #KAI# '),
        (ku_regex, ' #KU# '),
        (mune_regex, ' #MUNE# '),
        (chome_regex, ' #CHOME# '), # Catch chome / ban / go individually.
        (ban_regex, ' #BAN# '),
        (go_regex, ' #GO# '),
        (postal_regex, ' #POSTAL# '),
        (endgo_regex, ' #ENDGO# ')
        ]

    def __init__(self):
        pass

    def normalize(self, pattern, substitution, text):
        matches = [match[0] for match in re.findall(pattern, text)]
        for match in matches:
            text = text.replace(match, substitution)
        return matches, ' '.join(text.split()).strip()

    def tokenize(self, addr, use_char=False, return_str=False):
        """
        Returns an address object.
        """
        # Go through the regex and keep the group matches.
        regex_matches = defaultdict(list)
        for pattern, substitute in self.JAPANESE_ADDRESS_REGEXES:
            matches, addr = self.normalize(pattern, substitute, addr)
            regex_matches[substitute.strip()] = matches

        # Options to return different tokens.
        if use_char: # Split the non-captured groups by characters.
            tokens = list(chain(*[[token] if token.strip().startswith('#')
                                             and token.strip().endswith('#')
                                          else list(token)
                                   for token in addr.split()]))
        else: # Simply return the tokens split by spaces.
            tokens = addr.split()

        # Replace the placeholders back.
        for k in regex_matches:
            for v in regex_matches[k]:
                tokens[tokens.index(k)] = v

        address = Address(to=regex_matches['#TO#'], kai=regex_matches['#KAI#'],
                    ku=regex_matches['#KU#'], mune=regex_matches['#MUNE#'],
                    chome=regex_matches['#CHOME#'], ban=regex_matches['#BAN#'],
                    go=regex_matches['#GO#'], postal=regex_matches['#POSTAL#'],
                    endgo=regex_matches['#ENDGO#'], tokens=tokens)

        return ' '.join(address.tokens) if return_str else address
