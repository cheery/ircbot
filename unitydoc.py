import json
import re

with open('unitydoc.json') as fd:
    doc = json.load(fd)

common = doc['common']
info = doc['info']
pages = doc['pages']
searchIndex = doc['searchIndex']

def GetPageTitle(i):
    return pages[info[i][1]][1]

def GetPageURL(i):
    return pages[info[i][1]][0]

def GetPageSummary(i):
    return info[i][0]

def GetSearchResults(terms, query):
    score = {}
    min_score = len(terms)
    found_common = []
    for term in terms:
        if term in common:
            found_common.append(term)
        min_score -= 1
        if term in searchIndex:
            for page in searchIndex[term]:
                score[page] = score.get(page, 0) + 1
            for si in searchIndex:
                if si[0:len(term)] == term:
                    for page in searchIndex[term]:
                        score[page] = score.get(page, 0) + 1
    results = []
    for page in score:
        title = GetPageTitle(page)
        summary = GetPageSummary(page)
        url = GetPageURL(page)
        # ignore partial matches
        if score[page] >= min_score:
            # Adjust scores for better matches
            for term in terms:
                placement = title.lower().find(term)
                if placement >= 0:
                    score[page] += 50
                    if placement == 0 or title[placement - 1] == '.':
                        score[page] += 500
                    if placement + len(term) == len(title) or title[placement + len(term)] == '.':
                        score[page] += 500
                else:
                    placement = summary.lower().find(term)
                    if placement >= 0:
                        score[page] += 20 - placement if placement < 10 else 10
            if title.lower() == query:
                score[page] += 10000
            else:
                placement = title.lower().find(query)
                if placement >= 0:
                    score[page] += 200 - placement if placement < 100 else 100
                else:
                    placement = summary.lower().find(query)
                    if placement >= 0:
                        score[page] += 50 - placement if placement < 25 else 25
            results.append((
                -score[page],
                GetPageTitle(page).lower(),
                GetPageURL(page),
                GetPageSummary(page)))
    return results

def PerformSearch(query):
    query = query.strip().lower()
    terms = re.split(r"[\s.]+", query)
    combined = re.sub(r"\s+", '', query).lower()
    results = GetSearchResults(terms, query)
    results += GetSearchResults([combined], query)

    return sorted(list(set(results)))
