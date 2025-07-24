import matplotlib.pyplot as plt
import math
from matplotlib.patches import Circle, Arc
import numpy as np
import random
from collections import deque

fig, ax = plt.subplots()
ax.set_aspect('equal')  # 保持纵横比一致


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def point_on_circle(center, radius, angle_deg):
    """
    计算圆上指定角度（度数）的点坐标

    参数:
        center: 圆心坐标 (x, y)
        radius: 半径
        angle_deg: 角度（0° 表示正东方向，逆时针增加）

    返回:
        (x, y): 圆上的点坐标
    """
    angle_rad = math.radians(angle_deg)  # 将角度转换为弧度
    x = center[0] + radius * np.cos(angle_rad)
    y = center[1] + radius * np.sin(angle_rad)
    return (x, y)


def calculate_angle(center, point):
    """
    计算点到圆心的连线在极坐标中的角度（0°为正东，逆时针增加）

    参数:
        center: 圆心坐标 (xc, yc)
        point: 点坐标 (xp, yp)

    返回:
        角度（单位：度，范围 [-180°, 180°] 或 [0°, 360°]）
    """
    dx = point[0] - center[0]
    dy = point[1] - center[1]
    angle_rad = np.arctan2(dy, dx)  # 弧度（范围 [-π, π]）
    angle_deg = np.degrees(angle_rad)  # 转换为度

    # 可选：将角度转换为 [0°, 360°] 范围
    angle_deg = angle_deg % 360
    return angle_deg


def circle_intersection(point1, point2, r):
    """
    计算两个半径相等的圆的交点。
    返回:
        - None: 无交点（相离/重合）
        - [(x, y)]: 1 个交点（相切）
        - [(x1, y1), (x2, y2)]: 2 个交点
    """
    dx, dy = point2[0] - point1[0], point2[1] - point1[1]
    d_squared = dx ** 2 + dy ** 2
    d = np.sqrt(d_squared)

    # 检查相交条件
    if d > 2 * r or (d == 0 and r == 0):
        return None
    if d == 0:
        return None  # 重合

    # 计算垂直向量和偏移量
    u, v = -dy, dx  # 垂直方向向量
    h = np.sqrt(r ** 2 - (d_squared / 4))

    # 中点坐标
    x_m = (point1[0] + point2[0]) / 2
    y_m = (point1[1] + point2[1]) / 2

    # 交点
    x_a = x_m + (h * u) / d
    y_a = y_m + (h * v) / d
    x_b = x_m - (h * u) / d
    y_b = y_m - (h * v) / d

    # 处理相切情况（1 个交点）
    if np.isclose(d, 2 * r):
        return [(x_a, y_a), (x_a, y_a)]

    return [(x_a, y_a), (x_b, y_b)]


def deciding_clockwise(center, point, poi):
    """
    判断在核心圆上从交点 poi 出发，顺时针（True）还是逆时针（False）能得到优弧。

    参数:
        center: 核心圆圆心 (x, y)
        point: 另一个圆圆心 (x, y)
        poi: 交点坐标 (x, y)
        r: 圆的半径（两圆半径相同）

    返回:
        True（顺时针优弧） 或 False（逆时针优弧）
    """
    # 计算向量 v1 (center -> poi) 和 v2 (center -> point)
    v1 = np.array([poi[0] - center[0], poi[1] - center[1]])
    v2 = np.array([point[0] - center[0], point[1] - center[1]])

    # 计算叉积（v1 × v2）
    cross = np.cross(v1, v2)

    # 叉积符号决定方向
    return cross > 0  # True: 顺时针；False: 逆时针


def creating_cluster(points, r):
    """
    基于 BFS 的聚类算法：
    1. 对于每个未聚类的点，启动 BFS 搜索所有距离 ≤2r 的点。
    2. 将这些点归为同一簇。

    参数:
        points: 点集 [(x1, y1), (x2, y2), ...]
        r: 判定半径（两点距离 ≤2r 则归为同一簇）

    返回:
        clusters: 聚类结果 [[簇1], [簇2], ...]
    """
    if not points:
        return []

    clusters = []
    visited = set()  # 记录已访问的点

    for point in points:
        if tuple(point) in visited:
            continue  # 跳过已处理的点

        # 启动 BFS 搜索当前点的所有可达点
        cluster = []
        queue = deque([point])
        visited.add(tuple(point))

        while queue:
            current = queue.popleft()
            cluster.append(current)

            # 遍历所有未访问点，检查是否可加入当前簇
            for p in points:
                p_tuple = tuple(p)
                if p_tuple not in visited and distance(current, p) <= 2 * r:
                    visited.add(p_tuple)
                    queue.append(p)

        clusters.append(cluster)

    return clusters


def processing_cluster(cluster, r, actual_point=False, point_density=1):
    if len(cluster) == 1:
        trajs = [[]]
        traj = trajs[0]
        for theta in np.arange(0, 360, point_density):
            current_point = point_on_circle(cluster[0], r, theta)
            traj.append(current_point)
        if not actual_point:
            circle = Circle(cluster[0], r, fill=False, linewidth=2, color='red')
            ax.add_patch(circle)
        return trajs

    # 计算交点的角度并保存到point_table
    point_table = []# 注：正东为0度，角度随逆时针增加。
    for i in range(len(cluster)):
        point_table.append([])
        for j in range(len(cluster)):
            if i == j:
                continue
            if distance(cluster[i], cluster[j]) <= 2 * r:
                point1, point2 = circle_intersection(cluster[i], cluster[j], r)
                point_table[i].append([j, point1, 1])
                point_table[i].append([j, point2, 1])

    # 计算是“好点”还是“坏点”（好点在轨迹外部，会且只会经过一次；坏点在轨迹内部，不会被经过）
    for i in range(len(point_table)):
        for j in range(len(point_table[i])):
            isGoodpoint = True
            testing_point = point_table[i][j][1]
            for k in range(len(cluster)):
                if i == k or point_table[i][j][0] == k:
                    continue
                if distance(cluster[k], testing_point) <= r:
                    point_table[i][j][2] = 0
                    isGoodpoint = False
                    break
            if isGoodpoint:
                ax.plot(testing_point[0], testing_point[1], 'ro', markersize=8)
            else:
                ax.plot(testing_point[0], testing_point[1], 'go', markersize=6, zorder=1)

    # 对point_table中所有的点计算其角度,并按照角度排序
    for i in range(len(point_table)):
        for point_info in point_table[i]:
            angle = calculate_angle(cluster[i], point_info[1])
            point_info.append(angle)
        point_table[i].sort(key=lambda x: x[3])

    # 绘制边界
    trajs = []
    for i in range(len(point_table)):
        for j in range(len(point_table[i])):
            if not point_table[i][j][2]:
                continue
            # 选取当前点作为起始点
            traj = []
            x = i
            y = j
            while point_table[x][y][2]:
                point_table[x][y][2] = 0

                clockwise = deciding_clockwise(cluster[x], cluster[point_table[x][y][0]], point_table[x][y][1])
                y1 = y
                if clockwise:
                    while not point_table[x][y1][2]:
                        y1 -= 1
                    theta1 = point_table[x][y1][3]
                    theta2 = point_table[x][y][3]
                    next_point_index = y1
                else:
                    while not point_table[x][y1][2]:
                        y1 = (y + 1) % len(point_table[x])
                    theta1 = point_table[x][y][3]
                    theta2 = point_table[x][y1][3]
                    next_point_index = y1
                next_point = point_table[x][next_point_index][1]

                if not actual_point:
                    arc = Arc(cluster[x], 2 * r, 2 * r, angle=0, theta1=theta1, theta2=theta2,
                              linewidth=2, color='red')
                    ax.add_patch(arc)
                theta1 = math.ceil(theta1)
                theta2 = math.floor(theta2)
                traj.append(point_table[x][y][1])
                if theta1 > theta2:
                    theta2 += 360
                for theta in np.arange(theta1, theta2+1, point_density):
                    current_point = point_on_circle(cluster[x], r, theta)
                    traj.append(current_point)
                traj.append(next_point)

                point_table[x][next_point_index][2] = 0

                x = point_table[x][next_point_index][0]

                for z in range(len(point_table[x])):
                    if point_table[x][z][1] == next_point:
                        y = z
            trajs.append(traj)

    return trajs

def main():
    r = 8
    points = [(random.uniform(-25, 25), random.uniform(-25, 25)) for _ in range(8)]
    # points = [(7,7),(-7,7),(7,-7),(-7,-7)]
    actual_point = True  # True显示实际返回的点，不连续；False显示理论上的轨迹。
    point_density = 1  # 数值越小，返回的点越密，计算开销越大。默认为1，建议范围：0.1-45

    # 画圆
    for point in points:
        circle = Circle(point, r, fill=False, linewidth=2, color='lightblue', zorder=0)
        ax.add_patch(circle)

    point_cluster = creating_cluster(points, r)
    print('clusters:', point_cluster)
    print('points:', points)

    trajs = []
    for cluster in point_cluster:
        trajs.extend(processing_cluster(cluster, r, actual_point, point_density))
    if actual_point:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color'][:8]
        for i, traj in enumerate(trajs):
            color = colors[i%8]
            if point_density >= 5:
                markersize = 3
            else:
                markersize = 1
            for point in traj:
                ax.plot(point[0], point[1], 'o', color=color, markersize=markersize)

    plt.title("Border Problem")
    ax.autoscale()
    plt.show()


if __name__ == '__main__':
    main()
