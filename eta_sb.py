import numpy as np

data = np.load('data.npy')
months = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
times = np.array([9, 10.5, 12, 13.5, 15])
D = np.array([-59, -28, 0, 31, 61, 92, 122, 153, 184, 214, 245, 275])
plus = np.array([[-6, 6], [6, 6], [-6, -6], [6, -6]])
S = 0
X = []
Y = []
sideS = []
s_save = []
result = np.zeros(3332)

for i in range(12):
    for j in range(5):
        d = D[i]
        sin_rou = np.sin(2 * np.pi * d / 365) * np.sin(2 * (np.pi / 360) * 23.45)
        omiga = np.pi / 12 * (times[j] - 12)
        sin_as = np.cos(np.arcsin(sin_rou)) * np.cos((39.4 / 180) * np.pi) * np.cos(omiga) + sin_rou * np.sin((39.4 / 180) * np.pi)
        cos_ys = (sin_rou - sin_as * np.sin((39.4 / 180) * np.pi)) / (np.cos(np.arcsin(sin_rou)) * np.cos((39.4 / 180) * np.pi))
        I = np.array([-np.cos(np.arcsin(sin_as)) * np.sin(np.arccos(cos_ys)), -np.cos(np.arcsin(sin_as)) * cos_ys, -np.sin(np.arccos(cos_ys))])
        for k in range(3332):
            TA = outmat(data[k, 0:3], I)
            for l in range(3332):
                if np.sqrt((data[k, 0] - data[l, 0]) ** 2 + (data[k, 1] - data[l, 1]) ** 2 + (data[k, 2] - data[l, 2]) ** 2) < 50 and l != k:
                    TB = outmat(data[l, 0:3], I)
                    sideS_ = outS(TA, TB, data[k, 0:3], data[l, 0:3], I, 3, 3)
                    result[l] = result[l] + sideS_

        exec("result" + str(i + 1) + "_" + str(j + 1) + " = result")
        result = np.zeros(3332)

def outmat(R, I):
    R = np.array([-R[0], -R[1], 84 - R[2]])
    n = (R - I) / np.linalg.norm(R - I)
    cos_fi = n[2]
    fi = np.arccos(cos_fi)
    theta = np.arccos(n[1] / (-np.sin(fi)))
    aipu = np.array([np.cos(fi), np.sin(fi), 0])
    y = np.array([-np.cos(fi) * np.sin(theta), np.cos(fi) * np.cos(theta), np.sin(fi)])
    T = np.column_stack((aipu, y, n))
    return T

def cal(Ta, Tb, La, A, B, I):
    H1_ = np.dot(Tb, La) + A
    H2__ = np.dot(Tb.T, (H1_ - B))
    abc = np.dot(Tb, I.T)
    x_tou = H2__[0] - (abc[0] / abc[2]) * H2__[2]
    y_tou = H2__[1] - (abc[1] / abc[2]) * H2__[2]
    r = np.array([x_tou, y_tou])
    return r

def outS(Ta, Tb, Ra, Rb, I, a, b):
    r1 = cal(Ta, Tb, np.array([a / 2, b / 2, 0]), Ra, Rb, I)
    r2 = cal(Ta, Tb, np.array([-a / 2, b / 2, 0]), Ra, Rb, I)
    r3 = cal(Ta, Tb, np.array([-a / 2, -b / 2, 0]), Ra, Rb, I)
    r4 = cal(Ta, Tb, np.array([a / 2, -b / 2, 0]), Ra, Rb, I)
    r_ = np.column_stack((r1, r2, r3, r4))
    for i in range(4):
        if r_[0, i] > -a / 2 and r_[0, i] < a / 2 and r_[1, i] > -b / 2 and r_[1, i] < b / 2:
            zero__ = cal(Ta, Tb, np.array([0, 0, 0]), Ra, Rb, I)
            if zero__[0] > 0 and zero__[1] > 0:
                m = 1
            elif zero__[0] < 0 and zero__[1] > 0:
                m = 2
            elif zero__[0] < 0 and zero__[1] < 0:
                m = 3
            else:
                m = 4
        else:
            m = 0
        if m == 0:
            sideS = 0
        elif m == 1:
            sideS = (a / 2 - r_[0, i]) * (b / 2 - r_[0, i])
        elif m == 2:
            sideS = (a / 2 + r_[0, i]) * (b / 2 - r_[0, i])
        elif m == 3:
            sideS = (a / 2 + r_[0, i]) * (b / 2 + r_[1, i])
        else:
            sideS = (a / 2 - r_[0, i]) * (b / 2 + r_[1, i])
    return sideS
