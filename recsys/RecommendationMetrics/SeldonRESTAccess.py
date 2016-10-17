import requests
import json
from tqdm import tqdm
HOST=''

def get_token(consumer_key='', consumer_secret=''):
    """
    Gets seldon api token
    :param consumer_key: Consumer key fot the api
    :type consumer_key: str
    :param consumer_secret: Consumer secret for the api
    :type consumer_secret: str
    :rtype: str
    """
    token_uri = '/token?consumer_key={}&consumer_secret={}'.format(consumer_key, consumer_secret)
    response = requests.post(HOST+token_uri,{})
    content = response.json()
    return content.get('access_token')

def post_action(user,item, token):
    """
    Posts an action
    :param user: User who makes the action
    :type user: int
    :param item: Interacted item
    :type user: int
    :rtype: bool
    """
    action_uri = '/actions?oauth_token={}'.format(token)
    body = {'user':str(user), 'item':str(item), "type":0, "value": 0}
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    response = requests.post(HOST+action_uri,json.dumps(body), headers=headers)
    if response.status_code == 200:
        return True

def get_recommendation(algorithm, user, token, limit):
    """
    Gets Recommendation for a specific user
    :type algorithm: str
    :param algorithm: Algorithm used in the recommendation
    :type user: str
    :param user: User for the recommendation
    :type token: str
    :param token: Token used by the app
    :return:
    """
    recomm_uri = '/users/{}/recommendations?oauth_token={}&algorithms=recommenders:{}'.format(user,token,algorithm)
    print "Recom %s" %(recomm_uri)
    response = requests.get(HOST+recomm_uri)
    return json.loads(response.text)

def get_recommendation_id(users, algorithm, limit, token):
    """
    Gets the recommendations for a list of users
    :param users: Users to get a recommendation
    :type users: list
    :param algorithm: Algorithm for the recommendation
    :type algorithm: str
    :param limit: Limit of elements for the recommendation
    :type limit: int
    :return:
    """
    recommendations = []
    empty_recom = []
    print "Users Recommendation requests"
    mycount = 0
    for user in tqdm(users):
        recommendation_list = []
        recommendation = get_recommendation(algorithm, user, token, limit)
        recommendations_per_user = recommendation.get('list')
        mycount+=len(recommendations_per_user)
        if len(recommendations_per_user) == 0:
            empty_recom.append(user)
        else:
            for element in recommendations_per_user:
                recommendation_list.append(int(element.get('id')))
            recommendations.append({'recommendation': recommendation_list, 'user': user})
    print "List of users with empty recommendation"
    print empty_recom
    print "Actual recommendations = %i/%i" %(mycount, limit*len(users))
    
    return recommendations
