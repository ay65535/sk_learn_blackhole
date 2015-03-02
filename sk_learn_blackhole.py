# -*- coding: utf-8 -*-
# c.f. http://qiita.com/puriketu99/items/c519a95c0b16ea63c1ac
from sklearn.svm import LinearSVC
from sklearn.ensemble import AdaBoostClassifier, ExtraTreesClassifier, GradientBoostingClassifier, \
    RandomForestClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn import datasets
from sklearn.cross_validation import cross_val_score


# 学習データを用意する
iris = datasets.load_iris()  # ライブラリ付属のサンプルデータ
features = iris.data  # 特徴量のデータ
# 上記の分類の例でいうと、天気、場所、月日や各マンガを読んだかどうかに相当します
labels = iris.target  # 特徴量に対する正解データ
# 上記の分類の例でいうと、気温や性別に相当します

# 特徴量の次元を圧縮
# 似たような性質の特徴を同じものとして扱います
lsa = TruncatedSVD(2)
reduced_features = lsa.fit_transform(features)

# どのモデルがいいのかよくわからないから目があったやつとりあえずデフォルト設定で全員皆殺し
clf_names = ["LinearSVC", "AdaBoostClassifier", "ExtraTreesClassifier", "GradientBoostingClassifier",
             "RandomForestClassifier"]
for clf_name in clf_names:
    clf = eval("%s()" % clf_name)
    scores = cross_val_score(clf, reduced_features, labels, cv=5)
    score = sum(scores) / len(scores)  # モデルの正解率を計測
    print "%sのスコア:%s" % (clf_name, score)

# LinearSVCのスコア:0.973333333333
# AdaBoostClassifierのスコア:0.973333333333
# ExtraTreesClassifierのスコア:0.973333333333
# GradientBoostingClassifierのスコア:0.966666666667
# RandomForestClassifierのスコア:0.933333333333
