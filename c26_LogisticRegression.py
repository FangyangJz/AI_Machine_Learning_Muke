# !/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
created by Fangyang on Time:2018/7/12
'''

__author__ = 'Fangyang'

import numpy as np
from c3_accuracy_score import accuracy_score


class LogisticRegression(object):

    def __init__(self):
        self.coef_ = None
        self.interception_ = None
        self._theta = None

    def predict(self, x_predict):
        ''' 给定待测数据集X_predict, 返回表示X_predict的结果向量'''
        assert self.interception_ is not None and self.coef_ is not None,\
            'must fit before predict !'
        assert x_predict.shape[1] == len(self.coef_), \
            'the feature number of x_predict must be equal to x_train'

        proba = self.predict_prob(x_predict)
        return np.array(proba>=0.5, dtype='int')

    def predict_prob(self, x_predict):
        ''' 给定待测数据集X_predict, 返回表示X_predict的结果向量'''
        assert self.interception_ is not None and self.coef_ is not None,\
            'must fit before predict !'
        assert x_predict.shape[1] == len(self.coef_), \
            'the feature number of x_predict must be equal to x_train'

        X_b = np.hstack([np.ones((len(x_predict), 1)), x_predict])
        return self._sigmoid(X_b.dot(self._theta))

    def score(self, X_test, y_test):
        ''' 根据测试数据集 X_test 和 y_test 确定当前模型的准确度'''
        y_predict = self.predict(X_test)
        return accuracy_score(y_test, y_predict)

    def __repr__(self):
        return "LogisticRegression()"

    def _sigmoid(self, t):
        return 1. / (1. + np.exp(-t))

    def fit(self, X_train, y_train, eta=0.01, n_iters=1e4):
        '''根据训练数据集X_train, y_train,使用梯度下降法训练模型'''
        assert X_train.shape[0] == y_train.shape[0], \
            'the size of X_train must be equal to the size of y_train'

        def J(theta, X_b, y):
            '''损失函数'''
            y_hat = self._sigmoid(X_b.dot(theta))
            try:
                return -(np.sum(y*np.log(y_hat) + (1-y)*np.log(1-y_hat)) / len(y))
            except:
                return float('inf')

        def dJ(theta, X_b, y):
            return X_b.T.dot(self._sigmoid(X_b.dot(theta)) - y) / len(y)

        def gradient_descent(X_b, y, initial_theta, eta, n_iters=1e4, epsilon=1e-8):
            theta = initial_theta
            i_iter = 0

            while i_iter < n_iters:
                gradient = dJ(theta, X_b, y)
                last_theta = theta
                theta = theta - eta * gradient

                if (abs(J(theta, X_b, y) - J(last_theta, X_b, y)) < epsilon):
                    break

                i_iter += 1
            return theta

        X_b = np.hstack([np.ones((len(X_train), 1)), X_train])
        initial_theta = np.zeros(X_b.shape[1])
        self._theta = gradient_descent(X_b, y_train, initial_theta, eta, n_iters)

        self.interception_ = self._theta[0]
        self.coef_ = self._theta[1:]

        return self
    

