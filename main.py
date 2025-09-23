import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

from collections import deque
from Node import Node

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class main(object):

    # Carregar imagem do grid
    img = mpimg.imread("./assets/teste.png")

    #--------------------------------------------------------------------------
    # SUCESSORES PARA GRID
    #--------------------------------------------------------------------------
    # SUCESSORES PARA GRID (LISTA DE ADJACENCIAS)
    def sucessores_grid(self,st,nx,ny,mapa):
        f = []
        x, y = st[0], st[1]
        # DIREITA
        if y+1<ny:
            if mapa[x][y+1]==0:
                suc = []
                suc.append(x)
                suc.append(y+1)
                f.append(suc)
        # ESQUERDA
        if y-1>=0:
            if mapa[x][y-1]==0:
                suc = []
                suc.append(x)
                suc.append(y-1)
                f.append(suc)
        # ABAIXO
        if x+1<nx:
            if mapa[x+1][y]==0:
                suc = []
                suc.append(x+1)
                suc.append(y)
                f.append(suc)
        # ACIMA
        if x-1>=0:
            if mapa[x-1][y]==0:
                suc = []
                suc.append(x-1)
                suc.append(y)
                f.append(suc)

        return f

    #--------------------------------------------------------------------------
    # BUSCA EM AMPLITUDE
    #--------------------------------------------------------------------------
    def amplitude(self,inicio,fim,nx,ny,mapa):  # grid
        # Finaliza se início for igual a objetivo
        if inicio == fim:
            return [inicio]
        
        # GRID: transforma em tupla
        t_inicio = tuple(inicio)   # grid
        t_fim = tuple(fim)         # grid
        
        # Lista para árvore de busca - FILA
        fila = deque()

        # Inclui início como nó raíz da árvore de busca
        raiz = Node(None,t_inicio,0,None,None)  # grid
        fila.append(raiz)

        # Marca início como visitado
        visitado = {tuple(inicio): raiz}    # grid
        
        while fila:
            # Remove o primeiro da FILA
            atual = fila.popleft()
        
            # Gera sucessores a partir do grid
            filhos = self.sucessores_grid(atual.estado,nx,ny,mapa) # grid

            for novo in filhos:
                t_novo = tuple(novo)       # grid
                if t_novo not in visitado: # grid
                    filho = Node(atual,t_novo,atual.v1 + 1,None,None) # grid
                    fila.append(filho)
                    visitado[t_novo] = filho # grid
                    
                    # Verifica se encontrou o objetivo
                    if t_novo == t_fim:    # grid
                        return self.exibirCaminho(filho)
        return None


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
        (3, 8),
        (2, 7),
        (3, 2),
    ]

    # --------------------------
    # CRIA JANELA
    # --------------------------
    root = tk.Tk()
    root.title("Buscas")

    origem_label = tk.Label(root, text="Selecione a origem:")
    origem_label.pack()

    origem_combobox = ttk.Combobox(root, values=["0", "1"])
    origem_combobox.pack()

    destino_label = tk.Label(root, text="Selecione o destino:")
    destino_label.pack()

    destino_combobox = ttk.Combobox(root, values=["0", "1"])
    destino_combobox.pack()

    metodo_label = tk.Label(root, text="Selecione um método:")
    metodo_label.pack()

    metodo_combobox = ttk.Combobox(root, values=["AMPLITUDE"])
    metodo_combobox.pack()

    def metodosBusca(metodo_combobox, origem_combobox, destino_combobox):
        option = metodo_combobox.get()
        inicio = origem_combobox.get()
        fim = destino_combobox.get()

        if option == "AMPLITUDE":
            caminho = amplitude(self, inicio, fim, 10, 10, grid)
    #    elif(option = "PROFUNDIDADE"):

    #    elif(option = "PROFUNDIDADE LIMITADA"):

    #    elif(option = "APROFUNDAMENTO INTERATIVO"):

    #    else(option = "BIDIRECIONAL"):

    #    elif(option = "CUSTO UNIFORME"):
    #    elif(option = "GREEDY"):
    #    elif(option = "A*"):
    #    else(option = "AIA*"):


    plot_button = tk.Button(root, text="Enviar", command=metodosBusca(metodo_combobox, origem_combobox, destino_combobox))
    plot_button.pack()

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    root.mainloop()
    #plt.imshow(img, extent=[0, 10, 0, 10])  # fundo com imagem
    #plt.imshow(grid, cmap="tab20c", alpha=0.5, extent=[0, 10, 0, 10])  # grid semi-transparente

   
