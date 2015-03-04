#!/usr/bin/env python
# -*- coding: utf-8 -*-
# c.f. http://qiita.com/puriketu99/items/c519a95c0b16ea63c1ac
from sklearn.svm import LinearSVC
from sklearn.ensemble import AdaBoostClassifier, ExtraTreesClassifier, GradientBoostingClassifier, \
    RandomForestClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn import datasets
from sklearn.cross_validation import cross_val_score
import codecs
import sys
import csv


def sample_mysql_connector():
    import mysql.connector
    import keyring

    host_name = keyring.get_password('host_name', 'my_db_host')
    db_name = keyring.get_password('db_name', 'my_log_db')
    user_name = keyring.get_password('user_name', 'my_db_user')
    con = mysql.connector.connect(
        host=host_name,
        db=db_name,
        user=user_name,
        passwd=keyring.get_password(db_name, user_name),
        buffered=True)

    # 書き方が他と違うが、connect().cursor() 形式だとエラーになる模様
    cur = con.cursor()

    # cur.execute("SELECT l.time,lat,lng,acc,essid,bssid,rssi from \
    # LocationLog l left join wifi w on l.time = w.time \
    # where l.devid = 173 \
    # and l.time >= '2015-02-01 00:00' AND l.time < '2015-02-02 00:00'\
    # UNION\
    # SELECT l.time,lat,lng,acc,essid,bssid,rssi from\
    # LocationLog l right join wifi w on l.time = w.time\
    # where l.devid = 173\
    # and l.time >= '2015-02-01 00:00' AND l.time < '2015-02-02 00:00'")

    # 2015/02/01-2015/02/07の一週間分の位置情報とwifi情報
    cur.execute("""SELECT * FROM
LocationLog l LEFT JOIN wifi w ON l.time = w.time AND l.devid = w.devid
WHERE l.devid = 173
AND l.time >= '2015-02-01 00:00' AND l.time < '2015-02-08 00:00'
AND abs(l.time - provider_time) < 1000""")

    res = cur.fetchall()

    # for row in res:
    # print(row)

    cur.close()
    con.close()

    return res


argvs = sys.argv
argc = len(argvs)

print argvs
print argc
print

result = sample_mysql_connector()
exit()

if argc != 2:  # 引数が足りない場合は、その旨を表示
    print 'Usage: # python %s filename' % argvs[0]
    quit()

print 'The content of %s ...n' % argvs[1]

with open(argvs[1], 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーの読み飛ばし

    for line in reader:
        print line  # 1行づつlist表示

exit()

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
