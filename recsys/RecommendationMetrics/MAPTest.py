import numpy as np
from tqdm import tqdm

def average_precision(relevant_items, recommended, recomm_length):
    """
    Calculates the average precision for the specified recommendation_length.
    This function computes the average precision at recommendation_length between two lists of
    items.
    :type relevant_items: list
    :param relevant_items: Relevant items for the user
    :type recommended: list
    :param recommended: Items recommended for the user
    :type recomm_length: int
    :param recomm_length: Length of the recommendation
    :rtype: float
    """
    if len(recommended)>recomm_length:
        recommended = recommended[:recomm_length]
    score = 0.0
    num_hits = 0.0
    for i,p in enumerate(recommended):
        if p in relevant_items and p not in recommended[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)
    if not relevant_items:
        return 0.0
    return score / min(len(relevant_items), recomm_length)

def get_relevant_items(user, threshold, actions):
    """
    Gets the
    :param user: User to obtain relevant items
    :type user: str
    :param threshold: Threshold to separate relevant from non relevant
    :type threshold: float
    :rtype: ndarray
    """
    user_actions = actions[actions['user_id'] == user]
    relevant_user_items = user_actions[user_actions['value'] >= threshold]['item_id'].values.tolist()
    return relevant_user_items

def mean_average_precision(recommendations, users, threshold, actions, at):
    """
    Calculates the mean average precision
    :type recommendations: list
    :param recommendations: List of recommendations
    :type users: list
    :param users: Users for MAP
    :type threshold: float
    :param threshold: Relevant items threshold
    :return:
    """
    average_precisions = []
    print "Average Precission progress"
    for recommend in tqdm(recommendations):
        user_relevant_items = get_relevant_items(recommend.get('user'), threshold, actions)
        ap = average_precision(user_relevant_items, recommend.get('recommendation'),at)
        average_precisions.append(ap)
    return np.mean(average_precisions)