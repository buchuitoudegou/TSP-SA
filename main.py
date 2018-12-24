from SA import SA, City

def read_file(path):
  with open(path, 'r') as f:
    string = f.read()
    string = string.split('\n')
    result = []
    for s in string:
      eles = s.split(' ')
      temp = []
      for ele in eles:
        try:
          ele = int(ele)
          temp.append(ele)
        except:
          pass
      result.append(temp)
  return result


if __name__ == "__main__":
  result = read_file('instances/1.txt')
  solution = read_file('instances/best_1.txt')
  solution = list(map(lambda x: x[0], solution))
  # print(solution)
  cities = []
  for ele in result:
    cities.append(City(ele[1], ele[2], ele[0]))
  sa = SA(cities, solution)
  path, distance = sa.SA()
  print(distance, sa.best_distance, (distance - sa.best_distance) / sa.best_distance)