import tkinter as tk
from tkinter import ttk

from matplotlib import cm
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from collections import deque
from Node import Node
from BuscaP import busca

class BuscaNP(busca):
    #--------------------------------------------------------------------------
    # Criar a janela principal
    #--------------------------------------------------------------------------
    def __init__(self, janela):
        self.janela = janela
        self.canvas = None

        # Comboboxes
        opcoes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", 
                "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", 
                "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41"]

        metodos = ["AMPLITUDE", "PROFUNDIDADE", "PROFUNDIDADE LIMITADA",
        "APROFUNDAMENTO ITERATIVO", "BIDIRECIONAL", "CUSTO UNIFORME", "GREEDY", "A*", "AIA*"]

        self.label_origem = ttk.Label(self.janela, text="Selecione o ponto de origem:", font=("Arial", 12), foreground="black", background="#dfe3ee")
        self.label_origem.grid(row=1, column=0,  padx=20, pady=(0,0), sticky="ew")

        self.origem_combobox = ttk.Combobox(self.janela, values=opcoes, state="readonly")
        self.origem_combobox.grid(row=2, column=0, padx=20, pady=(2, 5), sticky="ew")

        self.label_destino = ttk.Label(self.janela, text="Selecione o ponto de destino:", font=("Arial", 12), foreground="black", background="#dfe3ee")
        self.label_destino.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        self.destino_combobox = ttk.Combobox(self.janela, values=opcoes, state="readonly")
        self.destino_combobox.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        self.label_metodo = ttk.Label(self.janela, text="Selecione o método de busca:", font=("Arial", 12), foreground="black", background="#dfe3ee")
        self.label_metodo.grid(row=5, column=0, padx=20, pady=5, sticky="ew")

        self.metodo_combobox = ttk.Combobox(self.janela, values=metodos, state="readonly")
        self.metodo_combobox.grid(row=6, column=0, padx=20, pady=(2, 5), sticky="ew")

        # Botão — agora dentro do __init__, então self existe
        self.botao = tk.Button(self.janela, text="Obter Valor", command=self.obter_valor_selecionado, background="#c1cff6", borderwidth=1,        # remove a borda do botão
        highlightthickness=0)
        self.botao.grid(row=7, column=0, columnspan=1, padx=5, pady=5, sticky="ew")


        # Configura expansão do grid
        self.janela.grid_columnconfigure(1, weight=1)
        self.janela.grid_rowconfigure(8, weight=1)
        self.janela.configure(background='#dfe3ee')
 
    #-----------------------------------------------------------------------------
    # GERA O GRID DE ARQUIVO TEXTO
    #-----------------------------------------------------------------------------
    def Gera_Problema_Grid_Fixo(self, arquivo):
        file = open(arquivo)
        mapa = []
        for line in file:
            aux_str = line.strip("\n")
            aux_str = aux_str.split(",")
            aux_int = [int(x) for x in aux_str]
            mapa.append(aux_int)
        nx = len(mapa)
        ny = len(mapa[0])
        return mapa,nx,ny

       #--------------------------------------------------------------------------
    # SUCESSORES PARA GRID
    #--------------------------------------------------------------------------
    # SUCESSORES PARA GRID (LISTA DE ADJACENCIAS)
    def sucessores_grid(self,st,nx,ny,mapa):
        f = []
        x, y = st[0], st[1]
        
        if mapa[x][y] == 9:
            return f
        
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
    
    #-------------------------------------------------------------------------- 
    # CONTROLE DE NÓS REPETIDOS
    #--------------------------------------------------------------------------
    def exibirCaminho1(self,encontro,visitado1, visitado2):
        t_encontro = tuple(encontro)
        # nó do lado do início
        encontro1 = visitado1[t_encontro]  
        # nó do lado do objetivo
        encontro2 = visitado2[t_encontro]
    
        caminho1 = self.exibirCaminho(encontro1)
        caminho2 = self.exibirCaminho(encontro2)
    
        # Inverte o caminho
        caminho2 = list(reversed(caminho2[:-1]))
    
        return caminho1 + caminho2
    
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
                t_novo = tuple(novo)   # grid
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

     #--------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------
    # BUSCA EM APROFUNDAMENTO ITERATIVO
    #--------------------------------------------------------------------------
    def aprof_iterativo(self,inicio,fim,nx,ny,mapa,lim_max):
        for lim in range(1,lim_max):
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
    
    #--------------------------------------------------------------------------
    # BUSCA BIDIRECIONAL
    #--------------------------------------------------------------------------
    def bidirecional(self,inicio,fim,nx,ny,mapa):
        if inicio == fim:
            return [inicio]
        
        # GRID: transforma em tupla
        t_inicio = tuple(inicio)   # grid
        t_fim = tuple(fim)         # grid

        # Lista para árvore de busca a partir da origem - FILA
        fila1 = deque()
        
        # Lista para árvore de busca a partir do destino - FILA
        fila2 = deque()
        
        # Inclui início e fim como nó raíz da árvore de busca
        raiz = Node(None,t_inicio,0,None,None)  # grid
        fila1.append(raiz)

        raiz = Node(None,t_fim,0,None,None)  # grid
        fila2.append(raiz)
    
        # Visitados mapeando estado -> Node (para reconstruir o caminho)
        visitado1 = {tuple(inicio): raiz}    # grid
        visitado2 = {tuple(fim): raiz}    # grid
        
        nivel = 0
        while fila1 and fila2:
            # ****** Executa AMPLITUDE a partir da ORIGEM *******
            # Quantidade de nós no nível atual
            nivel = len(fila1)  
            for _ in range(nivel):
                # Remove o primeiro da FILA
                atual = fila1.popleft()

                # Gera sucessores a partir do grid
                filhos = self.sucessores_grid(atual.estado,nx,ny,mapa) # grid

                for novo in filhos:
                    t_novo = tuple(novo)       # grid
                    if t_novo not in visitado1: # grid
                        filho = Node(atual,t_novo,atual.v1 + 1,None,None) # grid
                        visitado1[t_novo] = filho # grid

                        # Encontrou encontro com a outra AMPLITUDE
                        if t_novo in visitado2:    # grid
                            return self.exibirCaminho1(tuple(novo), visitado1, visitado2)

                        # Insere na FILA
                        fila1.append(filho)
            
            # ****** Executa AMPLITUDE a partir do OBJETIVO *******
            # Quantidade de nós no nível atual
            nivel = len(fila2)  
            for _ in range(nivel):
                # Remove o primeiro da FILA
                atual = fila2.popleft()
                
                # Gera sucessores a partir do grid
                filhos = self.sucessores_grid(atual.estado,nx,ny,mapa) # grid

                for novo in filhos:
                    t_novo = tuple(novo)       # grid
                    if t_novo not in visitado2: # grid
                        filho = Node(atual,t_novo,atual.v1 + 1,None,None) # grid
                        visitado2[t_novo] = filho # grid

                        # Encontrou encontro com a outra AMPLITUDE
                        if t_novo in visitado1:    # grid
                            return self.exibirCaminho1(t_novo, visitado1, visitado2)

                        # Insere na FILA
                        fila2.append(filho)
        return None

    def obter_valor_selecionado(self):
        origem = self.origem_combobox.get() 
        destino = self.destino_combobox.get()
        metodo = self.metodo_combobox.get()

        arquivo = "mapa1.txt"
        mapa, nx, ny = self.Gera_Problema_Grid_Fixo(arquivo)

        # Converte para posição no grid
        posicoes = {}
        arq = open("posicoes.txt")
        for aux in arq:
            linha = aux.strip().split()
            if len(linha) == 3:
                chave = linha[0]
                x = int(linha[1])
                y = int(linha[2])
                posicoes[chave] = (x, y)
                
        posicoes_inv = {v: k for k,v in posicoes.items()}   

        inicio = posicoes[origem]
        fim = posicoes[destino]

        caminho = None
        custo_str = 0
        if origem and destino and metodo:  # só se todos estiverem preenchidos
            if metodo == "AMPLITUDE":
                caminho = self.amplitude(inicio,fim,nx,ny,mapa)   # grid
            elif metodo == "PROFUNDIDADE":
                caminho = self.profundidade(inicio,fim,nx,ny,mapa)   # grid
            elif metodo == "PROFUNDIDADE LIMITADA":
                caminho = self.prof_limitada(inicio,fim,nx,ny,mapa, 4)
            elif metodo == "APROFUNDAMENTO INTERATIVO":
                caminho = self.aprof_iterativo(inicio,fim,nx,ny,mapa, 4)
            elif metodo == "BIDIRECIONAL":
                caminho = self.bidirecional(inicio,fim,nx,ny,mapa)
            elif metodo == "CUSTO UNIFORME":
                caminho = busca.custo_uniforme(self, inicio, fim, mapa, nx, ny)
            elif metodo == "GREEDY": 
                caminho = busca.greedy(self, inicio, fim, mapa, nx, ny)
            elif metodo == "A*":
                caminho = busca.a_estrela(self, inicio, fim, mapa, nx, ny)
            elif metodo == "AIA*":
                caminho = busca.aia_estrela(self, inicio, fim, mapa, nx, ny)
                
            if caminho:
                if type(caminho) == list:
                    caminho_str = " -> ".join(str(posicoes_inv[t]) for t in caminho)
                else:
                    caminho_str = " -> ".join(str(posicoes_inv[t]) for t in caminho[0])
                    custo_str += caminho[1]
            else:
                caminho_str = "Caminho não encontrado"
        
            # Criar figura do Matplotlib
            fig = Figure(figsize=(1, 1), dpi=100, facecolor="#dfe3ee")
            plot_fig = fig.add_subplot(111)
            
            # Recebe os pontos (x, y)
            plot_fig.imshow(mapa, cmap=cm.Greys, origin="upper")

            # Adicionar grid
            for x in range(nx + 1):
                plot_fig.axvline(x - 0.5, color="black", linewidth=0.5)
            for y in range(ny + 1):
                plot_fig.axhline(y - 0.5, color="black", linewidth=0.5)
            
            # Se houver caminho, desenha em vermelho
            if caminho:
                if type(caminho) == list:
                    xs, ys = zip(*caminho)
                elif caminho != None:
                    xs, ys = zip(*caminho[0])
                plot_fig.plot(ys, xs, color="red", linewidth=2, marker="o")

                destino_x, destino_y = xs[0], ys[0]
                plot_fig.annotate(
                    "Origem",
                    xy=(destino_y, destino_x),             # primeiro ponto
                    xytext=(destino_y+0.3, destino_x-0.3), # deslocamento do texto
                    arrowprops=dict(facecolor="green", shrink=0.05, width=2, headwidth=8),
                    fontsize=10,
                    color="green"
                )

                destino_x, destino_y = xs[-1], ys[-1]  # último ponto do caminho
                plot_fig.annotate(
                    "Destino",
                    xy=(destino_y, destino_x),
                    xytext=(destino_y+0.3, destino_x-0.3),
                    arrowprops=dict(facecolor="red", shrink=0.05, width=2, headwidth=8),
                    fontsize=10,
                    color="red"
                )


            # Inserir no Tkinter (grid) — substitui se já existir
            if self.canvas is not None:
                self.canvas.get_tk_widget().destroy()

            self.canvas = FigureCanvasTkAgg(fig, master=janela)
            self.canvas.get_tk_widget().grid(row=2, column=1, rowspan=7, padx=10, pady=0, sticky="nsew")

        # Exibe no Tkinter
        if hasattr(self, "caminho_label") and self.caminho_label is not None:
            self.caminho_label.destroy()

        if caminho is None:
            texto = caminho_str  # geralmente "Caminho não encontrado"
            cor = "red"
        else:
            # Se houver custo (como UCS), você pode ter custo_str
            if 'custo_str' in locals():
                texto = f"Caminho encontrado: {caminho_str} | Custo total: {custo_str}"
            else:
                texto = f"Caminho encontrado: {caminho_str}"
            cor = "black"

        # Cria/atualiza a label
        self.caminho_label = tk.Label(self.janela, text=texto, font=("Arial", 12), fg=cor, background="#dfe3ee")
        self.caminho_label.grid(row=0, column=1, columnspan=2, padx=10, pady=0)

# -------------------------
# CRIAR A JANELA E INICIAR
# -------------------------
if __name__ == "__main__":
    janela = tk.Tk()
    janela.title("Metodos de busca")
    app = BuscaNP(janela)
    janela.mainloop()