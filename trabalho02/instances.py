import numpy as np
from pathlib import Path
from typing import *
from math import ceil

# A primeira linha contém os numero de suppliers e o número de consummers, nessa ordem
# Em seguida, na segunda linha, estarão os valores dos estoques
# Depois, os valores de demanda dos clientes
# Finalmente a matriz com os valores de custo C_ij = custo de S_i para D_ij

def create_instances(shapes: List[Tuple[int,int]], random_state: int = None) -> None:
  if random_state != None:
    np.random.seed(random_state)

  output_folder = Path() / "instances"
  
  if not output_folder.exists() or output_folder.is_file():
    output_folder.mkdir()
  
  n_instances = len(shapes)
  
  for i in range(n_instances):
    with (output_folder / f'{i}_instance.txt').open('w') as file:
      n_suppliers, n_consumers = shapes[i]
      n_cost = n_suppliers * n_consumers
      cost = np.random.rand(n_cost) * np.random.randint(1,100,n_cost)
      np.round(cost, 2, out=cost)
      cost = cost.reshape((n_suppliers, n_consumers))
      demmand = np.random.randint(1, 1000, size=n_consumers)
      stock = np.random.randint(1, 1000, size=n_suppliers)

      if demmand.sum() > stock.sum():
        stock = stock + ceil((demmand.sum() - stock.sum()) / n_suppliers)

      file.write(' '.join(map(str,stock)) + '\n')
      file.write(' '.join(map(str,demmand)) + '\n')
      file.write('\n'.join(map(lambda l: ' '.join(map(str,l)), cost)))

      file.close()

def get_instances() -> Generator[Tuple[List[float], List[float], List[List[float]]], None, None]:
  for instance in reversed(list((Path() / "instances").glob("*_instance.txt"))):
    with instance.open("r") as file:
      S = np.loadtxt(file, max_rows=1)
      D = np.loadtxt(file, max_rows=1)
      C = np.loadtxt(file)

      file.close()

      yield (S,D,C)


if __name__ == '__main__':
  create_instances([(3,3),(3,2)],42)
  for S,D,C in get_instances():
    print(S)
    print(D)
    print(C)
