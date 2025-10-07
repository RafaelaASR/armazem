from collections import deque
from NodeP import NodeP

class busca(object):
    #--------------------------------------------------------------------------
    # SUCESSORES PARA GRID
    #--------------------------------------------------------------------------
    def sucessores_grid_ponderado(self,st,nx,ny,mapa):
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
                custo = 5
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        # ESQUERDA
        if y-1>=0:
            if mapa[x][y-1]==0:
                suc = []
                suc.append(x)
                suc.append(y-1)
                custo = 7
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        # ABAIXO
        if x+1<nx:
            if mapa[x+1][y]==0:
                suc = []
                suc.append(x+1)
                suc.append(y)
                custo = 2
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        # ACIMA
        if x-1>=0:
            if mapa[x-1][y]==0:
                suc = []
                suc.append(x-1)
                suc.append(y)
                custo = 29
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)        
        return f

    #--------------------------------------------------------------------------
    # DISTÂNCIA MANHATTAN
    #--------------------------------------------------------------------------

    def manhattan(self, atual, fim):
        x1, y1 = atual
        x2, y2 = fim
        return abs(x1 - x2) + abs(y1 - y2)

    #--------------------------------------------------------------------------    
    # INSERE NA LISTA MANTENDO-A ORDENADA
    #--------------------------------------------------------------------------    
    def inserir_ordenado(self,lista, no):
        for i, n in enumerate(lista):
            if no.v1 < n.v1:
                lista.insert(i, no)
                break
        else:
            lista.append(no)

    # -----------------------------------------------------------------------------
    # CUSTO UNIFORME
    # -----------------------------------------------------------------------------
    def custo_uniforme(self,inicio,fim,mapa,nx,ny):
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        t_inicio = tuple(inicio)   # grid
        raiz = NodeP(None, t_inicio,0, None, None, 0)  # grid
        lista.append(raiz)
    
        # Controle de nós visitados
        #visitado = {inicio: raiz}
        visitado = {tuple(inicio): raiz}    # grid
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
    
            # Chegou ao objetivo: UCS garante ótimo (custos >= 0)
            if atual.estado == fim:
                caminho = self.exibirCaminho(atual)
                return caminho, atual.v2
            
            # Gera sucessores a partir do grid
            filhos = self.sucessores_grid_ponderado(atual.estado,nx,ny,mapa) # grid
    
            for novo in filhos: # grid
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                v1 = v2 
    
                # Não visitado ou custo melhor
                t_novo = tuple(novo[0])       # grid
                if (t_novo not in visitado) or (v2<visitado[t_novo].v2): # grid
                    filho = NodeP(atual,t_novo, v1, None, None, v2) # grid
                    visitado[t_novo] = filho # grid
                    self.inserir_ordenado(lista, filho)
    
        # Sem caminho
        return None
    
    # -----------------------------------------------------------------------------
    # GREEDY
    # -----------------------------------------------------------------------------
    def greedy(self, inicio, fim, mapa, nx, ny):
            if inicio == fim:
                return [inicio]
            
            lista = deque()
            t_inicio = tuple(inicio)
            raiz = NodeP(None, t_inicio, 0, None, None, 0)
            lista.append(raiz)
            visitado = {inicio: raiz}
            
            while lista:
                atual = lista.popleft()
                valor_atual = atual.v2

                if visitado.get(atual.estado) is not atual:
                    continue

                if atual.estado == fim:
                    caminho = self.exibirCaminho(atual)
                    return caminho, atual.v2

                filhos = self.sucessores_grid_ponderado(atual.estado, nx, ny, mapa)

                for novo in filhos:
                    t_novo = tuple(novo[0])       # grid

                    v2 = valor_atual + novo[1]
                    v1 = self.manhattan(t_novo, fim)
                    
                    if (t_novo not in visitado) or (v2 < visitado[t_novo].v2):
                        filho = NodeP(atual, t_novo, v1, None, None, v2)
                        visitado[t_novo] = filho
                        self.inserir_ordenado(lista, filho)
            
            return None
    
    # -----------------------------------------------------------------------------
    # A ESTRELA
    # -----------------------------------------------------------------------------
    def a_estrela(self,inicio,fim,mapa,nx,ny):
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        t_inicio = tuple(inicio)
        
        raiz = NodeP(None, inicio, 0, None, None, 0)
    
        lista.append(raiz)
    
        # Controle de nós visitados
        visitado = {inicio: raiz}
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
    
            # Chegou ao objetivo
            if atual.estado == fim:
                caminho = self.exibirCaminho(atual)
                return caminho, atual.v2
    
            filhos = self.sucessores_grid_ponderado(atual.estado, nx, ny, mapa)
    
            for novo in filhos:
                pos = tuple(novo[0])
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                v1 = v2 + self.manhattan(pos,fim) 
    
                # relaxamento: nunca visto ou custo melhor
                if (pos not in visitado) or (v2 < visitado[pos].v2):
                    filho = NodeP(atual, pos, v1, None, None, v2)
                    visitado[pos] = filho
                    self.inserir_ordenado(lista, filho)
    
        # Sem caminho
        return None

    # ----------------------------------------------------------------------------
    # AI ESTRELA
    # -----------------------------------------------------------------------------       
    def aia_estrela(self,inicio,fim, mapa, nx, ny):
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        limite = self.manhattan(inicio,fim) 
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        
        # Busca iterativa
        while True:
            lim_acima = []
            
            raiz = NodeP(None, inicio, 0, None, None, 0)       
            lista.append(raiz)
        
            # Controle de nós visitados
            visitado = {inicio: raiz}

            while lista:
                # remove o primeiro nó
                atual = lista.popleft()
                valor_atual = atual.v2
                
                # Chegou ao objetivo
                if atual.estado == fim:
                    caminho = self.exibirCaminho(atual)
                    return caminho, atual.v2, limite
                
                filhos = self.sucessores_grid_ponderado(atual.estado, nx, ny, mapa)

                for novo in filhos:
                    pos = tuple(novo[0])
                    # custo acumulado até o sucessor
                    v2 = valor_atual + novo[1]
                    v1 = v2 + self.manhattan(pos,fim) 
                    
                    # Verifica se está dentro do limite
                    if v1<=limite:
                        # Não visitado ou custo melhor
                        if (pos not in visitado) or (v2 < visitado[pos].v2):
                            filho = NodeP(atual, pos, v1, None, None, v2)
                            visitado[pos] = filho
                            self.inserir_ordenado(lista, filho)
                    else:
                        lim_acima.append(v1)
            
            if len(lim_acima) != 0:
                limite = sum(lim_acima)/len(lim_acima)
            else:
                limite = 0
            lista.clear()
            visitado.clear()
            filhos.clear()
                        
        return 
    