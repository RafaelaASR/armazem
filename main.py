import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# Carregar imagem
img = mpimg.imread("./assets/teste.png")

# Criar grid fictício (10x10)
# 0 = livre, 9 obstáculo
grid = np.zeros((10, 10))
grid[-9, 4] = 9
grid[6, 2:7] = 9

path = [
    (4, 5),
    (6, 7),
    (7, 9),
    (8, 6),
    (8, 8),
    (2,7),
    (3,11),
]

fig, ax = plt.subplots()

plt.imshow(img, extent=[0, 10, 0, 10])  # fundo com imagem
plt.imshow(grid, cmap="tab20c", alpha=0.5, extent=[0, 10, 0, 10])  # grid semi-transparente

y,x = zip(*path)
ax.plot(x, y, color="red", linewidth=2)
ax.scatter(x, y, color="blue", s=50)

ax.scatter(x[0], y[3], color="green", s=100, label="Início")
ax.scatter(x[1], y[3], color="purple", s=100, label="Fim")

ax.legend()

plt.grid(True, color="white")  # linhas de grid
plt.show()
