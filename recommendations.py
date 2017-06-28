from math import sqrt


# A dictionary of movie critics and their ratings of a small
# set of movies.
# Although you can fit a large number of preferences in memory
# in a dictionary, for a very large dataset you'll probably want
# to store preferences in a database.
critics = {
    "User 01" : {
        "Titanic": 2.5,
        "Avengers": 3.5,
        "Slumdog Millionaire": 3.0,
        "Superman Returns": 3.5,
        "You, Me and Dupree": 2.5,
        "The Night Listener": 3.0
    },
    "User 02": {
        "Titanic": 3.0,
        "Avengers": 3.5,
        "Slumdog Millionaire": 1.5,
        "Superman Returns": 5.0,
        "You, Me and Dupree": 3.5,
        "The Night Listener": 3.0
    },
    "User 03": {
        "Titanic": 2.5,
        "Avengers": 3.0,
        "Superman Returns": 3.5,
        "The Night Listener": 4.0
    },
    "User 04": {
        "Avengers": 3.5,
        "Slumdog Millionaire": 3.0,
        "Superman Returns": 4.0,
        "You, Me and Dupree": 2.5,
        "The Night Listener": 4.5
    },
    "User 05": {
        "Titanic": 3.0,
        "Avengers": 4.0,
        "Slumdog Millionaire": 2.0,
        "Superman Returns": 3.0,
        "You, Me and Dupree": 2.0,
        "The Night Listener": 3.0
    },
    "User 06": {
        "Titanic": 3.0,
        "Avengers": 4.0,
        "Superman Returns": 5.0,
        "You, Me and Dupree": 3.5,
        "The Night Listener": 3.0
    },
    "User 07": {
        "Avengers": 4.5,
        "Superman Returns": 4.0,
        "You, Me and Dupree": 1.0,
    }
}


# Returns a distance-based similarity score for person1 and
# person2
def sim_distance(prefs, person1, person2):
    # Get the list of shared items
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    
    # if they have no rating in common
    # return 0
    if len(si) == 0: return 0
    
    # Add up the squares of all the 
    # differences
    sum_of_squares = sum([pow(prefs[person1][item] - 
                         prefs[person2][item], 2)
                         for item in si])
    
    return 1 / (1 + sum_of_squares)


# Returns the Pearson correlation for person1 and person2
def sim_pearson(prefs, person1, person2):
    # Get the list of shared items
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    
    # Find the number of elements
    n = len(si)
    
    # if they have no rating in common
    # return 0
    if len(si) == 0: return 0
    
    # Add up all the preferences
    sum1 = sum([prefs[person1][it] for it in si])
    sum2 = sum([prefs[person2][it] for it in si])
    
    # Sum up the squares
    sum1Sq = sum([pow(prefs[person1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[person2][it], 2) for it in si])
    
    # Sum up the products
    pSum = sum([prefs[person1][it] * prefs[person2][it] for it in si])
    
    # Calculate Pearson score
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0
    
    r = num / den
    
    return r

# Returns the best matches for person from prefs dictionary.
# Number of results and similarity function are optinal params.
def top_matches(prefs, person, n = 5, similarity = sim_pearson):
    scores = [(similarity(prefs, person, other), other) 
                for other in prefs if other!=person]
    
    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
# Totals[item] => hold sum of similarity_i * review_i for item not 
# reviewed by person
# simSums[item] => hold the sum of similarity_i for item not reviewed
# by person. Note: critics who didn't reviewed the item are not added.
def getRecommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSums = {}
    
    for other in prefs:
        # don't compare person to itself
        if person == other: continue
        sim = similarity(prefs, person, other)
        
        # ignore scores of zero or lower
        if sim <= 0: continue
        for item in prefs[other]:
            
            # only score movies person haven't
            # seen but other seen 
            if item not in prefs[person] or prefs[person][item] == 0:
                # similarity * score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim
    
    # Create the normalized list
    # ranking of ith item = totals[item_i]/simSums[item_i]
    rankings = [(total/simSums[item], item) for item, total in totals.items()]
    
    # return the sorted list
    rankings.sort(reverse=True)
    return rankings

# to understand run transformPrefs(recommendations.critics) on
# command line and compare them to critics dictionary
def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            
            result[item][person] = prefs[person][item]
    return result