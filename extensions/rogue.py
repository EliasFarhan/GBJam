import random
from engine.const import log
from engine.vector import Vector2

__author__ = 'efarhan'

random.seed(0)

def random_add(rogue_map, type_nmb, radius):
    size = Vector2(len(rogue_map),len(rogue_map[0]))
    for i in range(size.x):
        for j in range(size.y):
            dice_value = random.random()
            radius_list = range(radius+1)
            radius_list.extend(map((lambda n: -n),range(1,radius+1)))
            for x in radius_list:
                for y in radius_list:
                    rogue_map[(i-x)%size.x][(j-y)%size.y] += dice_value
    for i in range(size.x):
        for j in range(size.y):
            rogue_map[i][j] = int(rogue_map[i][j]/((2*radius+1)**2)*type_nmb)

def linear_distribution(rogue_map, type_nmb, radius):
    size = Vector2(len(rogue_map),len(rogue_map[0]))
    #generate map
    for i in range(size.x):
        for j in range(size.y):
            log(str(i)+" "+str(j))
            around_tile = [0 for x in range(type_nmb)]
            radius_list = range(radius+1)
            radius_list.extend(map((lambda n: -n),range(1,radius+1)))
            for x in radius_list:
                for y in radius_list:
                    if rogue_map[(i-x)%size.x][(j-y)%size.y] == 0:
                        continue
                    else:
                        around_tile[rogue_map[(i-x)%size.x][(j-y)%size.y]-1]+=1
            total_value = 0
            for x in around_tile:
                total_value += x+1
            dice_value = random.random()
            tile_index = 0


            prob = 0.0
            while prob+(float(around_tile[tile_index]+1)/total_value) < dice_value:
                #log(str(dice_value)+str(around_tile)+str(tile_index))
                prob += (float(around_tile[tile_index]+1)/total_value)
                tile_index+=1
            rogue_map[i][j] = tile_index+1
def generate_map(size=Vector2(100,100),type_nmb=3, radius=1,func=random_add):
    rogue_map = [[0 for j in range(size.y)] for i in range(size.x)]
    func(rogue_map,type_nmb,radius)

    return rogue_map

if __name__ == '__main__':
    log(generate_map(size=Vector2(20,20)))