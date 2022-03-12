


from re import A


def downpoints(points,percent):
    if len(points)== 1:
        return points[0]
    result = []
    for e in range(len(points)-1):
        newpoint = [points[e][0]*percent + points[e+1][0]*(1-percent), points[e][1]*percent + points[e+1][1]*(1-percent)]
        result.append(newpoint)
    return downpoints(result,percent)

def besierline(points,count):
    result = []
    for e in range(count):
        result.append(downpoints(points,e/count))
    return result

def besierline_percent(points_1,points_2,percent,count):
    newpoints = []
    for e in range(max([len(points_1),len(points_2)])):
        point = [int(points_1[e][0] * percent + points_2[e][0]*(float(1)-percent)),int(points_1[e][1] * percent + points_2[e][1]*(float(1)-percent))]
        newpoints.append(point)
    result = besierline(newpoints,count)
    return result