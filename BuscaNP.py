import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
from Node import Node

class BuscaNP(object):
    #--------------------------------------------------------------------------
    # Criar a janela principal
    #--------------------------------------------------------------------------
    def __init__(self, janela):
        self.janela = janela
        self.canvas = None

        # Comboboxes
        opcoes = ["0", "2", "3"]
        metodos = ["AMPLITUDE", "PROFUNDIDADE", "PROFUNDIDADE LIMITADA"]

        self.origem_combobox = ttk.Combobox(self.janela, values=opcoes, state="readonly")
        self.origem_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.destino_combobox = ttk.Combobox(self.janela, values=opcoes, state="readonly")
        self.destino_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.metodo_combobox = ttk.Combobox(self.janela, values=metodos, state="readonly")
        self.metodo_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Botão — agora dentro do __init__, então self existe
        self.botao = tk.Button(self.janela, text="Obter Valor", command=self.obter_valor_selecionado)
        self.botao.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Configura expansão do grid
        self.janela.grid_columnconfigure(0, weight=1)
        self.janela.grid_rowconfigure(0, weight=1)

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
    # EXIBE O CAMINHO ENCONTRADO NA ÁRVORE DE BUSCA
    #--------------------------------------------------------------------------    
    def exibirCaminho(self,node):
        caminho = []
        while node is not None:
            caminho.append(node.estado)
            node = node.pai
        caminho.reverse()
        return caminho
    
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

    #--------------------------------------------------------------------------
    # BUSCA EM PROFUNDIDADE
    #--------------------------------------------------------------------------
    def profundidade(self,inicio,fim,nx,ny,mapa):
        # Finaliza se início for igual a objetivo
        if inicio == fim:
            return [inicio]
        
        # GRID: transforma em tupla
        t_inicio = tuple(inicio)   # grid
        t_fim = tuple(fim)         # grid
        
        # Lista para árvore de busca - FILA
        pilha = deque()
    
        # Inclui início como nó raíz da árvore de busca
        raiz = Node(None,t_inicio,0,None,None)  # grid
        pilha.append(raiz)
    
        # Marca início como visitado
        visitado = {tuple(inicio): raiz}    # grid
        
        while pilha:
            # Remove o primeiro da FILA
            atual = pilha.pop()
    
            # Gera sucessores a partir do grid
            filhos = self.sucessores_grid(atual.estado,nx,ny,mapa) # grid
    
            for novo in filhos:
                t_novo = tuple(novo)       # grid
                if t_novo not in visitado: # grid
                    filho = Node(atual,t_novo,atual.v1 + 1,None,None) # grid
                    pilha.append(filho)
                    visitado[t_novo] = filho # grid
                    
                    # Verifica se encontrou o objetivo
                    if t_novo == t_fim:    # grid
                        return self.exibirCaminho(filho)
        return None
    
    #--------------------------------------------------------------------------
    # BUSCA EM PROFUNDIDADE LIMITADA
    #--------------------------------------------------------------------------
    def prof_limitada(self,inicio,fim,nx,ny,mapa,lim):
        # Finaliza se início for igual a objetivo
        if inicio == fim:
            return [inicio]
        
        # GRID: transforma em tupla
        t_inicio = tuple(inicio)   # grid
        t_fim = tuple(fim)         # grid
        
        # Lista para árvore de busca - FILA
        pilha = deque()
    
        # Inclui início como nó raíz da árvore de busca
        raiz = Node(None,t_inicio,0,None,None)  # grid
        pilha.append(raiz)
    
        # Marca início como visitado
        visitado = {tuple(inicio): raiz}    # grid
        
        while pilha:
            # Remove o primeiro da FILA
            atual = pilha.pop()
            
            if atual.v1<lim:
                # Gera sucessores a partir do grid
                filhos = self.sucessores_grid(atual.estado,nx,ny,mapa) # grid
        
                for novo in filhos:
                    t_novo = tuple(novo)       # grid
                    if t_novo not in visitado: # grid
                        filho = Node(atual,t_novo,atual.v1 + 1,None,None) # grid
                        pilha.append(filho)
                        visitado[t_novo] = filho # grid
                        
                        # Verifica se encontrou o objetivo
                        if t_novo == t_fim:    # grid
                            return self.exibirCaminho(filho)
        return None

    def obter_valor_selecionado(self):
        origem = self.origem_combobox.get() 
        destino = self.destino_combobox.get()
        metodo = self.metodo_combobox.get()
        caminho = None
        mapa = [
            [0, 0, 1],
            [0, 1, 0],
            [0, 0, 0]
        ]

        # Converte para posição no grid
        posicoes = {
            "0": (0, 0),
            "2": (0, 1),
            "3": (1, 0)
        }

        inicio = posicoes[origem]
        fim = posicoes[destino]

        nx = len(mapa)
        ny = len(mapa[0])

        if origem and destino and metodo:  # só se todos estiverem preenchidos
            if metodo == "AMPLITUDE":
                self.amplitude(inicio,fim,nx,ny,mapa)   # grid
            elif metodo == "PROFUNDIDADE":
                self.profundidade(inicio,fim,nx,ny,mapa)   # grid
            elif metodo == "PROFUNDIDADE LIMITADA":
                self.prof_limitada(inicio,fim,nx,ny,mapa, 4)
          
            # Criar figura do Matplotlib
            fig = Figure(figsize=(5, 4), dpi=100)
            plot_fig = fig.add_subplot(111)

            # Exemplo de gráfico (pode trocar para grafo de arestas depois)
            plot_fig.plot([0, 1, 2, 3], [int(origem), 2, 3, int(destino)])

            # Inserir no Tkinter (grid) — substitui se já existir
            if self.canvas is not None:
                self.canvas.get_tk_widget().destroy()

            self.canvas = FigureCanvasTkAgg(fig, master=janela)
            self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=4, padx=10, pady=5, sticky="nsew")


# -------------------------
# CRIAR A JANELA E INICIAR
# -------------------------
if __name__ == "__main__":
    janela = tk.Tk()
    app = BuscaNP(janela)
    janela.mainloop()