import numpy as np
from pathlib import Path

# A primeira linha contém os numero de suppliers e o número de consummers, nessa ordem
# Em seguida, na segunda linha, estarão os valores dos estoques
# Depois, os valores de demanda dos clientes
# Finalmente a matriz com os valores de custo C_ij = custo de S_i para D_ij

def instance_generator(shapes, random_state=None):
  if random_state != None:
    np.random.seed(random_state)

  output_folder = Path() / "instances"
  
  if not output_folder.exists() or output_folder.is_file():
    output_folder.mkdir()
  
  n_instances = len(shapes)
  
  for i in range(n_instances):
    
    with open(f'instances/{i}.txt', 'w') as file:
      n_suppliers, n_consumers = shapes[i]
      n_cost = n_suppliers * n_consumers
      cost = np.random.rand(n_cost) * np.random.randint(1,100,n_cost)
      np.round(cost, 5, out=cost)
      cost = cost.reshape((n_suppliers, n_consumers))
      demmand = np.random.randint(1, 1000, size=n_consumers)
      stock = np.random.randint(1, 1000, size=n_suppliers)

      if demmand.sum() > stock.sum():
        stock = stock + (demmand.sum() - stock.sum())

      file.write(f'{n_suppliers} {n_consumers}\n')
      
      for s in range(n_suppliers):
        if (s == n_suppliers-1):
          file.write(str(stock[s]) + '\n')
        else:
          file.write(str(stock[s]) + ' ')
      
      for d in range(n_consumers):
        if (d == n_consumers-1):
          file.write(str(demmand[d]) + '\n')
        else:
          file.write(str(demmand[d]) + ' ')
      
      for s in range(n_suppliers):
        for c in range(n_consumers):
          if c == n_consumers-1:
            file.write(f'{cost[s][c]}\n')
          else:
            file.write(f'{cost[s][c]} ')
      
      file.close()

def instances():
  for instance in reversed([ f for f in (Path() / "instances").glob("*.txt") ]):
    file = instance.open("r")
    
    ns, nd = tuple([ float(n) for n in file.readline().split(' ') ])
    s = [ e for e in map(float, file.readline().split(' ')) ]
    d = [ e for e in map(float, file.readline().split(' ')) ]
    c = [ [ e for e in map(float, arr.split(' ')) ] for arr in  file.readlines() ]
    
    file.close()

    yield ns,nd,s,d,c

if __name__ == '__main__':
  shapes = {
    0: (100,100),
    1: (200,150),
    2: (150,200)
  }

  instance_generator(shapes=shapes, random_state=42)
