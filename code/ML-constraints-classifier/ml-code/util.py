from collections import Counter
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix


def data_info(y_train, y_test):
    num_train = len(y_train)
    y_trn_counter = Counter(y_train)
    num_pos_trn = y_trn_counter[1]
    num_neg_trn = y_trn_counter[0]
    num_test = len(y_test)
    y_test_counter = Counter(y_test)
    num_pos_test = y_test_counter[1]
    num_neg_test = y_test_counter[0]
    return [num_train, num_pos_trn, num_neg_trn, num_test, num_pos_test, num_neg_test]


def evaluation_report(y_test, y_pred):
    precision = precision_score(y_test, y_pred) * 100
    recall = recall_score(y_test, y_pred) * 100
    accuracy = accuracy_score(y_test, y_pred) * 100
    f1 = f1_score(y_test, y_pred) * 100
    return [precision, recall, f1, accuracy]