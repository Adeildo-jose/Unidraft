from usuario import GerenciadorUsuarios
from interface import Interface
from seletivasatleta import MenuTreinador, MenuAtleta


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
                Interface.exibir_e_aguardar("\nEsporte salvo com sucesso!")
            else:
                Interface.exibir_e_aguardar("Opção inválida!")
        except ValueError:
            Interface.exibir_e_aguardar("Entrada inválida! Digite um número.")


class MenuUsuario:

    def __init__(self, autenticacao, email):
        self.autenticacao = autenticacao
        self.email = email
        self.esporte_manager = Esporte()
        self.gerenciador = GerenciadorUsuarios()

    def exibir_esporte_marcado(self):
        esporte = self.esporte_manager.obter_esporte(self.email)
        if esporte:
            print(f"\nEsporte marcado: {esporte}")
        else:
            print("\nVocê ainda não marcou nenhum esporte.")

    def executar_menu(self):
        while True:
            usuario = self.gerenciador.obter_usuario(self.email)
            funcao = usuario.funcao
            esporte = usuario.esporte

            Interface.limpar_tela()
            print("_" * 50)
            print("MENU\n")
            print("_" * 50)
            print("\n[1] Ver esporte marcado")
            print("[2] Marcar esporte")
            print("[3] Seletivas")
            print("[4] Editar dados da conta")
            print("[5] Excluir conta")
            print("[0] Sair\n")

            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                Interface.limpar_tela()
                self.exibir_esporte_marcado()
                Interface.pausa_com_clear()

            elif escolha == "2":
                Interface.limpar_tela()
                self.esporte_manager.selecionar_esporte(self.email)

            elif escolha == "3":
                Interface.limpar_tela()
                if funcao == "Técnico":
                    menu_seletivas = MenuTreinador(self.email, esporte)
                else:
                    menu_seletivas = MenuAtleta(self.email, esporte)
                menu_seletivas.executar_menu()

            elif escolha == "4":
                Interface.limpar_tela()
                self.autenticacao.editar_dados()

            elif escolha == "5":
                if self.autenticacao.excluir_conta():
                    break

            elif escolha == "0":
                Interface.exibir_e_aguardar("Saindo do menu. Até mais!", 1.0)
                break

            else:
                Interface.exibir_e_aguardar("Opção inválida. Tente novamente.")

            Interface.limpar_tela()
