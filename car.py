import math

def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def point_intersect(A, B, C, D):
    first_vector = (B[0] - A[0], B[1] - A[1])
    second_vector = (D[0] - C[0], D[1] - C[1])

    dist_x = (A[0] - C[0]) / (second_vector[0] - first_vector[0])
    dist_y = (A[1] - C[1]) / (second_vector[1] - first_vector[1])

    x = A[0] + first_vector[0] * dist_x
    y = A[1] + first_vector[1] * dist_y
    return (x, y)

def dist_intersect(A, B, C, D,reach):
    if not intersect(A,B,C,D):
        #print("flag",A,B,C,D)
        return 1

    first_vector = (B[0] - A[0], B[1] - A[1])
    second_vector = (D[0] - C[0], D[1] - C[1])


    dist_x = (A[0] - C[0]) / (second_vector[0] - first_vector[0])
    dist_y = (A[1] - C[1]) / (second_vector[1] - first_vector[1])

    x = first_vector[0] * dist_x
    y = first_vector[1] * dist_y

    output = (x**2+y**2)**0.5

    return 1-output/reach-0.1

class Car:
    def __init__(self,brain,id):
        #self.positions=[[300, 300], [300, 360], [320, 360]]
        #self.positions=[[200, 160], [200, 220], [220, 220]]
        self.positions=[[260, 160], [260, 180], [200, 180]]
        self.angle=0
        self.isAlive=True
        self.brain=brain

        self.id=id

        self.checkpoints_passed=1

        self.last_des=0

    def getCenter(self):
        return [(self.positions[0][0] + self.positions[2][0]) / 2, (self.positions[0][1] + self.positions[2][1]) / 2]
    def advance_car(self, speed=1):
        advance_x = math.cos(math.radians(self.angle))
        advance_y = math.sin(math.radians(self.angle))
        # print(angle,advance_x,advance_y)
        for point in self.positions:
            point[0] += advance_x * speed
            point[1] -= advance_y * speed

    def turn_car(self,turn):
        self.angle-=turn
        center = self.getCenter()
        for i in self.positions:
            i[0] -= center[0]
            i[1] -= center[1]

            i[0] = i[0] * math.cos(math.radians(turn)) - i[1] * math.sin(math.radians(turn))
            i[1] = i[0] * math.sin(math.radians(turn)) + i[1] * math.cos(math.radians(turn))

            i[0] += center[0]
            i[1] += center[1]

    def detectCollision(self, death_lines, checklines):
        last_x = self.positions[2][0] + (self.positions[0][0] - self.positions[1][0])
        last_y = self.positions[2][1] + (self.positions[0][1] - self.positions[1][1])

        nextCheck=checklines[self.checkpoints_passed]
        if intersect(self.positions[0], self.positions[2], nextCheck[0], nextCheck[1]) or intersect(self.positions[1], (last_x,last_y), nextCheck[0], nextCheck[1]):
            self.checkpoints_passed+=1
        for death_line in death_lines:
            if self.checkpoints_passed>1:
                intersect_prev=intersect(self.positions[0], self.positions[1], death_line[self.checkpoints_passed-2], death_line[self.checkpoints_passed-1]) or intersect(self.positions[2], (last_x,last_y), death_line[self.checkpoints_passed-2], death_line[self.checkpoints_passed-1])
            else:
                intersect_prev=False
            intersect_next=intersect(self.positions[0], self.positions[1], death_line[self.checkpoints_passed-1], death_line[self.checkpoints_passed]) or intersect(self.positions[2], (last_x,last_y), death_line[self.checkpoints_passed-1], death_line[self.checkpoints_passed])
            if intersect_next or intersect_prev:
                self.isAlive=False
                self.deathPoint=self.positions[0]
                return True
        return False

    def range_points(self,leng):
        center=self.getCenter()
        output=[]

        for i in range(-2,3):
            ang=self.angle+i*30
            x,y=math.cos(math.radians(ang))*leng , math.sin(math.radians(ang))*leng
            output.append((int(center[0]+x),int(center[1]-y)))

        return output
    def collision_distances(self,death_lines,reach):
        center=self.getCenter()
        #print(self.range_points())
        out=[]
        for A in self.range_points(reach):
            add=1
            for death_line in death_lines:
                for i in range(len(death_line)-1):
                    add=min(add,dist_intersect(A,center,death_line[i],death_line[i+1],reach))
            out.append(add)
        return out

    def takeDecision(self,death_lines=None,reach=100):

        data=self.collision_distances(death_lines,reach)
        decision=self.getMaxResult(self.brain.feedAll(data))
        self.last_des=decision
        if decision==1:
            self.turn_car(1)
        elif decision==2:
            self.turn_car(-1)

    def takeSameDecision(self):
        if self.last_des==1:
            self.turn_car(1)
        elif self.last_des==2:
            self.turn_car(-1)

    def fitness(self,checkpoints):
        line_to_reach=checkpoints[self.checkpoints_passed]
        point_to_reach=((line_to_reach[0][0]+line_to_reach[1][0])/2,(line_to_reach[0][1]+line_to_reach[1][1])/2)

        distance_to_point=((point_to_reach[0]-self.deathPoint[0])**2+(point_to_reach[1]-self.deathPoint[1])**2)**0.5

        #print(self.checkpoints_passed , distance_to_point, (self.checkpoints_passed*10)**2-distance_to_point*10)
        return (self.checkpoints_passed*1000)-distance_to_point
    def getMaxResult(self,results):
        return results.index(max(results))