from usuario import GerenciadorUsuarios
from interface import Interface


class Esporte:

    
    ESPORTES_INDIVIDUAIS = {
        1: "Atletismo",
        2: "Atletismo Paralímpico",
        3: "Judô",
        4: "Judô Paralímpico",
        5: "Natação",
        6: "Natação Paralímpica",
        7: "Tênis de Mesa",
        8: "Tênis de Mesa em Cadeira de Rodas"
    }
    
    ESPORTES_COLETIVOS = {
        1: "Basquete",
        2: "Basquete de Cadeira de Rodas",
        3: "Futebol",
        4: "Futebol de 5",
        5: "Futsal",
        6: "Handebol",
        7: "Vôlei",
        8: "Vôlei Sentado"
    }
    
    def __init__(self):
        self.gerenciador = GerenciadorUsuarios()
    
    def salvar_esporte(self, email, esporte_nome):
      
        usuario = self.gerenciador.obter_usuario(email)
        if usuario:
            usuario.esporte = esporte_nome
            self.gerenciador.atualizar_usuario(email, usuario)
    
    def obter_esporte(self, email):
      
        usuario = self.gerenciador.obter_usuario(email)
        if usuario:
            return usuario.esporte
        return ""
    
    def selecionar_esporte(self, email):
        
        print("SELECIONE O ESPORTE")
        print("[1] Esportes Individuais")
        print("[2] Esportes Coletivos")
        print("[0] Voltar\n")
        tipo = input("Escolha: ")
        
        if tipo == "0":
            return
        elif tipo == "1":
            esportes = self.ESPORTES_INDIVIDUAIS
        elif tipo == "2":
            esportes = self.ESPORTES_COLETIVOS
        else:
            print("Opção inválida!")
            return
        
        print("\nOpções disponíveis:")
        for numero in esportes:
            print(f"[{numero}] {esportes[numero]}")
        
        try:
            esporte_escolhido = int(input("Escolha um esporte: "))
            
            if esporte_escolhido in esportes:
                nome_esporte = esportes[esporte_escolhido]
                print(f"\nVocê escolheu: {nome_esporte}")
                
                self.salvar_esporte(email, nome_esporte)
                Interface.exibir_e_aguardar("\n✓ Esporte salvo com sucesso!")
            else:
                Interface.exibir_e_aguardar("✗ Opção inválida!")
        except ValueError:
            Interface.exibir_e_aguardar("✗ Entrada inválida! Digite um número.")


class MenuUsuario:
    
    
    def __init__(self, autenticacao, email):
        self.autenticacao = autenticacao
        self.email = email
        self.esporte_manager = Esporte()
    
    def exibir_seletivas(self):
       
        esporte = self.esporte_manager.obter_esporte(self.email)
        if esporte:
            print(f"\nSeletivas marcadas:")
            print(f"Esporte: {esporte}")
        else:
            print("\nVocê ainda não marcou nenhuma seletiva.")
    
    def executar_menu(self):
       
        while True:
            print("_" * 50)
            print("MENU\n")
            print("_" * 50)
            print("\n[1] Ver seletivas marcadas")
            print("[2] Marcar seletiva")
            print("[3] Editar dados da conta")
            print("[4] Excluir conta\n")
            print("[0] Sair")
            
            escolha = input("Escolha uma opção: ")
            
            if escolha == "1":
                Interface.limpar_tela()
                self.exibir_seletivas()
                Interface.pausa_com_clear()
            elif escolha == "2":
                Interface.limpar_tela()
                self.esporte_manager.selecionar_esporte(self.email)
            elif escolha == "3":
                Interface.limpar_tela()
                self.autenticacao.editar_dados()
            elif escolha == "4":
                if self.autenticacao.excluir_conta():
                    break
            elif escolha == "0":
                Interface.exibir_e_aguardar("Saindo do menu. Até mais!", 1.0)
                break
            else:
                Interface.exibir_e_aguardar("✗ Opção inválida. Tente novamente.")
            
            Interface.limpar_tela()
