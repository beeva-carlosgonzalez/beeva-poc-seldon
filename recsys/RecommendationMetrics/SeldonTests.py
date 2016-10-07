import pandas as pd
import SeldonRESTAccess
from MAPTest import mean_average_precision
from tqdm import tqdm
import os, sys
import re
data_path = '' #os.path.dirname(os.path.abspath('__file__'))
from collections import defaultdict

def main(users=[], actions_compare_file='/testandvalidation.csv', threshold=3, limit=50, algorithm='MATRIX_FACTOR'):
    """
    MAP calculator when recent actions are not needed
    :param users: Users list to whom we will calculate MAP
    :param actions_compare_file: Test user actions file
    :param threshold: Threshold for relevant actions
    :param limit: Limit for the MAP calculation (k at MAP@K)
    :param algorithm: Algorithm to use
    :return:
    """
    global consumer_secret
    global consumer_key
    token = SeldonRESTAccess.get_token(consumer_key, consumer_secret)
    actions_path = data_path + '' + actions_compare_file
    actions = pd.read_csv(actions_path, sep='\t', names=['user_id', 'item_id', 'value', 'timestamp'])
    if len(users) == 0:
        users = set(actions.user_id.values.tolist())
    recomm_set = SeldonRESTAccess.get_recommendation_id(users, algorithm, limit, token)
    MAP = mean_average_precision(recomm_set, users, threshold, actions, limit)
    return MAP

def item_similarity_map(actions_insert_file='/movielens_100k_u1_train.csv' ,actions_compare_file='/testandvalidation.csv', threshold=3, limit=10):
    """
    Item similarity MAP
    :param actions_insert_file: User actions to be inserted as recent actions
    :param actions_compare_file: Test user actions file
    :param threshold:  Threshold for relevant actions
    :param limit: Limit for the MAP calculation (k at MAP@K)
    :return:
    """
    global consumer_secret
    global consumer_key
    token = SeldonRESTAccess.get_token(consumer_key, consumer_secret)
    actions_path = data_path + '' + actions_insert_file
    actions = pd.read_csv(actions_path, sep='\t', names=['user_id', 'item_id', 'value', 'timestamp'])
    actions = actions[actions['value'] >= threshold]
    print "Insertando Acciones"
    i=0
    counter=defaultdict(int)
    for index, action in tqdm(actions.iterrows()):
        counter[action['user_id']]+=1
        if counter[action['user_id']]<=10:
            #continue
            response = SeldonRESTAccess.post_action(action['user_id'],action['item_id'], token)
        i+=1
        #if i==100:
        #    break
        if not response:
            print "action for user {} with item {} went wrong".format(action['user_id'],action['item_id'])
    return main(actions_compare_file=actions_compare_file, threshold=threshold, limit=limit, algorithm= 'SIMILAR_ITEMS')

def compute_repeated_elements(recomm_set):
    actions_path = data_path + '/movielens_100k_u1_train.csv'
    actions = pd.read_csv(actions_path)
    repeated_list = []
    for recom in recomm_set:
        sum = 0
        for element in recom.get('recommendation'):
            if element in actions[recom.get('user')]:
                sum +=1
        repeated_list.append(sum)
    return repeated_list

if __name__ == '__main__':
    print "\nUsage example: \npython SeldonTests.py --host=http://localhost:8080 --algorithm=MATRIX_FACTOR --compareactionsfile=./data/u1_nano.test --consumerkey=$SELDONKEY --consumersecret=$SELDONSECRET\n"
    for arg in sys.argv:
        if re.search('--host=', arg):
            host = arg.replace('--host=', '')
            SeldonRESTAccess.HOST = host
        if re.search('--insertactionsfile=', arg):
            insert_file = arg.replace('--insertactionsfile=', '')
        if re.search('--compareactionsfile=', arg):
            compare_file = arg.replace('--compareactionsfile=', '')
        if re.search('--consumerkey=', arg):
            consumer_key = arg.replace('--consumerkey=', '')
        if re.search('--consumersecret=', arg):
            consumer_secret = arg.replace('--consumersecret=', '')
        if re.search('--algorithm=', arg):
            algorithm = arg.replace('--algorithm=', '')
    if algorithm == 'itemsimilarity':
        print item_similarity_map(actions_insert_file=insert_file, actions_compare_file=compare_file, threshold=3, limit=10)
    else:
        print main(actions_compare_file=compare_file, threshold=3, limit=10, algorithm='MATRIX_FACTOR')
