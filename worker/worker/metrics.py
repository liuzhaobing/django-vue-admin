# -*- coding:utf-8 -*-
from typing import Callable

from sklearn.metrics import *


def get_metrics(
        datas: list[dict],
        y_true_key: str,
        y_pred_key: str,
        metrics: list[Callable],
        average: str | None = None
):
    y_true, y_pred = [], []
    for item in datas:
        y_true.append(item[y_true_key])
        y_pred.append(item[y_pred_key])

    def calculate_not_none():
        _metric = {"average": f"{average}.{y_true_key}"}
        for metric in metrics:
            _metric[metric.__name__] = metric(
                y_true,
                y_pred,
                average=average,
                zero_division=1
            )
        return _metric

    if average is not None:
        return [calculate_not_none()]

    unique_ys = set(y_true)

    def calculate_one_topic_none(unique_y):
        _metric = {"average": f"{y_true_key}", y_true_key: unique_y}
        for metric in metrics:
            if metric in [
                recall_score,
                precision_score,
                f1_score
            ]:
                _metric[metric.__name__] = metric(
                    y_true,
                    y_pred,
                    labels=[unique_y],
                    average=average,
                    zero_division=1
                ).tolist()[0]
        return _metric

    return [calculate_one_topic_none(y) for y in unique_ys]
