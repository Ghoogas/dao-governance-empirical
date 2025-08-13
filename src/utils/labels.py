import re

def label_governance_model(space):
    text = (space.get('name','') + ' ' + space.get('about','')).lower()
    if re.search(r'delegate|delegation|representative', text): return 'delegated'
    if re.search(r'reputation|soulbound|non[-\s]?transferable', text): return 'reputation'
    if re.search(r'parameter|autonom|algorithmic|controller|rate module', text): return 'algorithmic'
    if re.search(r'snapshot|erc-20|one token one vote|token[-\s]?weighted', text): return 'token'
    return 'hybrid'
