from sklearn.metrics import precision_score, recall_score, f1_score, balanced_accuracy_score

def get_scores(y_true, y_pred):
    # avg = 'binary' if y_true.unique().shape[0] < 2 else 'macro'
    avg = 'binary'
    # bas = balanced_accuracy_score(y_true, y_pred)
    ps = precision_score(y_true, y_pred, zero_division=0, average=avg)
    rs = recall_score(y_true, y_pred, zero_division=0, average=avg)
    f1s = f1_score(y_true, y_pred, zero_division=0, average=avg)
    return {
        # 'Balanced Accuracy': bas,
        'Precision': ps,
        'Recall': rs,
        'F1 Score': f1s
    }

def print_scores(scores):
    for k, v in scores.items():
        print('{}: {:.5f}'.format(k, v))

def print_score_diff(scores1, scores2):
    for k1, v1, in scores1.items():
        print('{} Difference: {:.5f}'.format(k1, v1 - scores2[k1]))