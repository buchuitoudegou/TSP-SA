import copy
import random
from scipy import exp

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
    return ((c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2) ** 0.5

class SA():
  def __init__(self, cities, best_solution):
    self.cities = copy.deepcopy(cities)
    self.path = []
    self.best_solution = copy.deepcopy(best_solution)
    self.best_solution = list(map(lambda x: x - 1, self.best_solution))
    self.best_distance = self.evaluate(self.best_distance)
    self.distance = 0.0
    
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
        # print('a')
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
      distance += City.distance(self.cities[path[i]], self.cities[path[i + 1]])
      # print(path[i], end=' ')
      # print(self.cities[path[i]])
    return distance

  def SA(self):
    T = 100
    self.initial_path()
    self.distance = self.evaluate(self.path)
    while T > 0.000000001:
      print(T, self.distance)
      for i in range(1500):
        new_path = copy.deepcopy(self.path)
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
    return self.path, self.distance
