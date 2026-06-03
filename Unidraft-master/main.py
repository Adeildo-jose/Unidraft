from cadastro import Cadastro
from autenticacao import Autenticacao
from esportes import MenuUsuario
from interface import Interface


class SistemaUnidraft:
    
    def __init__(self):
        self.cadastro = Cadastro()
        self.autenticacao = Autenticacao()
    
    def exibir_menu_principal(self):
    
        print("_" * 50)
        print("\nBem-vindo ao Unidraft!")
        print("_" * 50)
        print("\n[1] Fazer cadastro")
        print("[2] Fazer login")
        print("[0] Sair\n")
        
        escolha = input("Escolha uma opção: ")
        return escolha
    
    def executar(self):
        
        Interface.limpar_tela()
        while True:
            escolha = self.exibir_menu_principal()
            
            if escolha == "1":
                Interface.limpar_tela()
                self.cadastro.fazer_cadastro()
                Interface.aguardar_com_clear()
            
            elif escolha == "2":
                Interface.limpar_tela()
                if self.autenticacao.fazer_login():
                    menu_usuario = MenuUsuario(self.autenticacao, self.autenticacao.usuario_logado.email)
                    menu_usuario.executar_menu()
                Interface.aguardar_com_clear(1.0)
            
            elif escolha == "0":
                Interface.exibir_e_aguardar("Saindo do sistema. Até mais!")
                break
            
            else:
                Interface.exibir_e_aguardar("Opção inválida. Tente novamente.")


def main():
   
    sistema = SistemaUnidraft()
    sistema.executar()


if __name__ == "__main__":
    main()
