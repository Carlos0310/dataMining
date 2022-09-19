from math import log
import operator
import pandas as pd
import plotTree

# 处理导入的数据
def ImportData(file):
    data1 = pd.read_excel(file)
    data = data1.iloc[:, :].values.tolist()
    b = data1.iloc[:, :]
    label = b.columns.values.tolist()
    # print(data)
    # print(label)
    return data, label


# 计算信息熵
def Ent(data):
    lendata = len(data)  # 数据条数
    label_num = {}  # 不同类别数目
    # print(data)
    for feat in data:
        cate = feat[-1]  # 叶子节点
        # print(cate)
        if cate not in label_num.keys():
            label_num[cate] = 0
        label_num[cate] += 1
    ent = 0
    print("当前分类：" + str(label_num))
    for key in label_num:
        k = float(label_num[key]) / lendata  # 计算单类熵值
        ent += k * log(k, 2)

    print("当前节点的初始信息熵：" + str(-ent))
    return -ent


def tags(data, i, value):
    tags = []
    for feat in data:
        if feat[i] == value:
            t = feat[:i]
            t.extend(feat[i + 1:])
            tags.append(t)
    print("按照特征 " + str(value) + " 分类后的数据：" + str(tags))
    return tags


def C45(data):
    num = len(data[0]) - 1  # 计算有几个特征
    print("当前选择的特征数："+ str(num))
    ent = Ent(data) # 计算初始信息熵
    best_gain = 0
    best_feat = -1
    for i in range(num):
        featlist = [row[i] for row in data]  # 某一列特征的所有值矩阵
        print(featlist)
        vals = set(featlist)
        ent1 = 0
        for k in vals:
            t = tags(data, i, k)  # 按照特征k 分类数据
            pro = len(t) / float(len(data))
            ent1 += pro * Ent(t)
        info = ent - ent1
        info_ent = Ent(t) # 计算信息熵
        if info_ent == 0:
            continue
        gain = info / info_ent # 计算信息增益率
        if (gain > best_gain):  # 将最大的信息增益赋给info
            best_gain = gain
            best_feat = i  # 将最大的信息增益相对应的特征下标赋给feat
    print("当前最大信息增益：" + str(best_gain))
    return best_feat


def get_max(list):
    count = {}
    for i in list:
        if i not in count.keys():
            count[i] = 0
        count[i] += 1
    class_count = sorted(count.items(), key=operator.itemgetter(1), reverse=True)
    print(class_count)
    return class_count[0][0]


def createTree(data, labels):
    classlist = [row[-1] for row in data]  # 取特征矩阵最后一列进行分类
    # print(classlist)
    if classlist.count(classlist[0]) == len(classlist):
        return classlist[0]
    if len(data[0]) == 1:  # 当data矩阵还剩最后一列时
        return get_max(classlist)
    best_feat = C45(data)  # 计算信息增益选择最优特征
    best_label = labels[best_feat]
    print("当前最优特征节点：" + str(best_label))
    myTree = {best_label: {}}
    del (labels[best_feat])  # 将选择的特征删除
    feat_values = [row[best_feat] for row in data]  # 当前最优特征的特征值
    # print(feat_values)
    vals = set(feat_values)
    for value in vals:
        t_labels = labels[:]
        myTree[best_label][value] = createTree(tags(data, best_feat, value), t_labels)
    # print(myTree)
    return myTree


if __name__ == '__main__':
    datafile = u'gua.xlsx'  # 数据文件
    data, labels = ImportData(datafile)
    myTree = createTree(data, labels)
    print("得到的树集合为：")
    print(myTree)
    plotTree.createPlot(myTree)