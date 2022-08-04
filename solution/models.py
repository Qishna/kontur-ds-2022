import numpy as np
import pandas as pd
from collections import defaultdict
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score, recall_score, precision_score, accuracy_score


class EnsembleClassifier:
    """Ensemble class of two classifiers."""

    def __init__(self, model1, model2, alpha=0.5):
        self._model1 = model1
        self._model2 = model2
        assert 0 <= alpha <= 1
        self._alpha = alpha

    def fit(self, x, y):
        self._model1.fit(x, y)
        self._model2.fit(x, y)

    def predict_proba(self, x):
        return self._model1.predict_proba(x) * self._alpha + self._model2.predict_proba(x) * (1 - self._alpha)

    def predict(self, x):
        return self.predict_proba(x)[:, 1] > 0.5


def get_features_df(texts_df, vectorizer) -> pd.DataFrame:
    """Extracting features from a dataframe."""
    features_arr = vectorizer.transform(texts_df).toarray()
    return pd.DataFrame(features_arr, columns=vectorizer.get_feature_names())


def get_metrics_k_fold(texts, targets, vectorizer, model, watch_metrics, random_state, folds_number):
    """Predicting on folds for a given model."""
    skf = StratifiedKFold(folds_number, shuffle=True,
                          random_state=random_state)
    metrics = defaultdict(list)

    texts = np.array(texts)
    targets = np.array(targets)

    for i, (train_index, test_index) in enumerate(skf.split(texts, targets)):
        texts_train = texts[train_index]
        texts_test = texts[test_index]

        targets_train = targets[train_index]
        targets_test = targets[test_index]

        vectorizer.fit(texts_train)

        features_train = get_features_df(texts_train, vectorizer)
        features_test = get_features_df(texts_test, vectorizer)

        model.fit(features_train, targets_train)

        predict_test = model.predict(features_test)

        for metric in watch_metrics:
            metrics[metric.__name__].append(metric(targets_test, predict_test))
        metrics['fold_num'].append(i)
        metrics['model'].append(model.__class__.__name__)

    return pd.DataFrame(metrics)
