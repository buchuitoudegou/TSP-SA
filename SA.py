import copy
import random
from scipy import exp, sqrt
import matplotlib.pyplot as plt

class City():
  """
  description: City class representing a city in the map
  
  attr x: coordinate of the city

  attr y: coordinate of the city

  attr id: the id of the city
  """
  def __init__(self, x, y, id_):
    self.id = id_
    self.x = x
    self.y = y
  
  @staticmethod
  def distance(c1, c2):
    """
    Calculate the distance between two city
    param c1: a city
    param type: City
    param c2: a city
    param type: City
    """
    d1 = (c1.x - c2.x) ** 2
    d2 = (c1.y - c2.y) ** 2
    return (d1 + d2) ** 0.5

class SA():
  def __init__(self, cities, best_solution):
    self.cities = copy.deepcopy(cities)
    self.path = []
    self.best_solution = copy.deepcopy(best_solution)
    self.best_solution = list(map(lambda x: x - 1, self.best_solution))
    self.each_distance = []
    for i in range(len(self.cities)):
      temp = []
      for j in range(len(self.cities)):
        temp.append(City.distance(self.cities[i], self.cities[j]))
      self.each_distance.append(temp)
    self.best_distance = self.evaluate(self.best_solution)
    self.distance = 0.0
    self.lines = None
    x = list(map(lambda a: a.x, self.cities))
    y = list(map(lambda a: a.y, self.cities))
    self.ax = plt.figure().add_subplot(1,1,1)
    self.ax.scatter(x, y, color='r')
    self.initial_path()
    self.display()
    
  def generate_new_path(self, path):
    method = random.randint(0, 3)
    if method == 0:
      p1 = 1 + random.randint(0, len(self.cities) - 2 - 1)
      p2 = 1 + random.randint(0, len(self.cities) - 2 - 1)
      path[p1], path[p2] = path[p2], path[p1]
    elif method == 1:
      p1 = 0
      p2 = 0
      while p2 <= p1:
        p1 = 1 + random.randint(0, len(self.cities) - 1 - 1)
        p2 = 1 + random.randint(0, len(self.cities) - 1 - 1)
      temp = path[p1:p2]
      temp.reverse()
      path[p1:p2] = temp
    elif method == 2:
      p1 = 0
      p2 = 0
      while p2 <= p1:
        p1 = 1 + random.randint(0, len(self.cities) - 2 - 1)
        p2 = 1 + random.randint(0, len(self.cities) - 2 - 1)
      origin = path[p1:p2]
      t1 = [origin[-1]]
      t2 = origin[:len(origin) - 1]
      origin = t1 + t2
      path[p1:p2] = origin
    elif method == 3:
      p1 = 0
      p2 = 0
      length = 5
      while abs(p2 - p1) < length:
        p1 = 1 + random.randint(0, len(self.cities) - 2 - length - 1)
        p2 = 1 + random.randint(0, len(self.cities) - 2 - length - 1)
      path[p1:p1 + 5], path[p2:p2 + 5] = path[p2:p2 + 5], path[p1:p1 + 5]

  def initial_path(self):
    for i in range(len(self.cities)):
      self.path.append(i)
    
  def evaluate(self, path):
    distance = 0.0
    for i in range(len(self.cities) - 1):
      # distance += City.distance(self.cities[path[i]], self.cities[path[i + 1]])
      distance += self.each_distance[path[i]][path[i + 1]]
    return distance

  def SA(self):
    T = 100
    # self.initial_path()
    self.distance = self.evaluate(self.path)
    while T > 0.001:
      print(T, self.distance)
      for i in range(5000):
        new_path = list(map(lambda x: x, self.path))
        self.generate_new_path(new_path)
        distance = self.evaluate(new_path)
        if distance < self.distance:
          self.path = new_path
          self.distance = distance
        else:
          delta = distance - self.distance
          probility = exp(-delta / T)
          if probility > random.random():
            self.path = new_path
            self.distance = distance
      T *= 0.98
      self.display()
    return self.path, self.distance
  
  def display(self):
    x_temp = [self.cities[self.path[i]].x for i in range(len(self.cities))]
    y_temp = [self.cities[self.path[i]].y for i in range(len(self.cities))]
    x_temp.append(x_temp[0])
    y_temp.append(y_temp[0])
    if self.lines != None:
      self.ax.lines.remove(self.lines[0])
    self.lines = self.ax.plot(x_temp, y_temp, color="b")
    plt.title(str((self.distance - self.best_distance) / self.best_distance * 100) + '%')
    plt.pause(0.00001)