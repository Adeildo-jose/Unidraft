import getpass
from usuario import  GerenciadorUsuarios
from cadastro import ValidadorDados
from interface import Interface


class Autenticacao:
   
    
    def __init__(self):
        self.gerenciador = GerenciadorUsuarios()
        self.validador = ValidadorDados()
        self.usuario_logado = None
    
    def pedir_email(self):
       
        while True:
            email = input("\nDigite seu email (ou 0 para voltar): ").strip()
            
            if email == "0":
                print("Voltando ao menu principal...")
                return None
            
            valido, mensagem = self.validador.validar_email(email)
            if not valido:
                print(f"{mensagem}\n")
                continue
            
            return email
    
    def pedir_senha(self):
       
        while True:
            senha = getpass.getpass("Digite sua senha: ")
            
            valido, mensagem = self.validador.validar_senha(senha)
            if not valido:
                print(f"{mensagem}\n")
                continue
            
            return senha
    
    def fazer_login(self):
        
        print("_" * 50)
        print("\nFAÇA SEU LOGIN\n")
        print("_" * 50)
        
        while True:
            email = self.pedir_email()
            
            if email is None:
                return False
            
            senha = self.pedir_senha()
            
            usuario = self.gerenciador.obter_usuario(email)
            
            if usuario and usuario.senha == senha:
                Interface.exibir_e_aguardar("\n Login realizado com sucesso! Bem-vindo ao Unidraft!", 1.5)
                self.usuario_logado = usuario
                return True
            
            Interface.exibir_e_aguardar("\n Email ou senha incorretos. Tente novamente.", 1.0)
    
    def editar_dados(self):
        
        if self.usuario_logado is None:
            print("Nenhum usuário logado!")
            return
        
        print("\n" + "_" * 50)
        print("EDITAR DADOS DA CONTA")
        print("_" * 50)
        print(f"\nNome atual: {self.usuario_logado.nome}")
        print(f"Email atual: {self.usuario_logado.email}")
        print(f"Modalidade atual: {self.usuario_logado.modalidade}")
        print(f"Função atual: {self.usuario_logado.funcao}")
        print("\n[1] Editar nome")
        print("[2] Editar senha")
        print("[3] Editar modalidade")
        print("[4] Editar função")
        print("[0] Voltar\n")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            novo_nome = input("Digite o novo nome: ")
            valido, mensagem = self.validador.validar_nome(novo_nome)
            if valido:
                self.usuario_logado.nome = novo_nome.strip()
                self.gerenciador.atualizar_usuario(self.usuario_logado.email, self.usuario_logado)
                Interface.exibir_e_aguardar(" Nome atualizado com sucesso!")
            else:
                Interface.exibir_e_aguardar(f" {mensagem}")
        
        elif opcao == "2":
            nova_senha = getpass.getpass("Digite a nova senha: ")
            valido, mensagem = self.validador.validar_senha(nova_senha)
            if valido:
                self.usuario_logado.senha = nova_senha
                self.gerenciador.atualizar_usuario(self.usuario_logado.email, self.usuario_logado)
                Interface.exibir_e_aguardar(" Senha atualizada com sucesso!")
            else:
                Interface.exibir_e_aguardar(f" {mensagem}")
        
        elif opcao == "3":
            print("\n[1] Masculino")
            print("[2] Feminino\n")
            escolha = input("Escolha a modalidade: ")
            if escolha == "1":
                self.usuario_logado.modalidade = "Masculino"
                self.gerenciador.atualizar_usuario(self.usuario_logado.email, self.usuario_logado)
                Interface.exibir_e_aguardar("✓ Modalidade atualizada com sucesso!")
            elif escolha == "2":
                self.usuario_logado.modalidade = "Feminino"
                self.gerenciador.atualizar_usuario(self.usuario_logado.email, self.usuario_logado)
                Interface.exibir_e_aguardar(" Modalidade atualizada com sucesso!")
            else:
                Interface.exibir_e_aguardar(" Opção inválida!")
        
        elif opcao == "4":
            print("\n[1] Atleta")
            print("[2] Técnico\n")
            escolha = input("Escolha a função: ")
            if escolha == "1":
                self.usuario_logado.funcao = "Atleta"
                self.gerenciador.atualizar_usuario(self.usuario_logado.email, self.usuario_logado)
                Interface.exibir_e_aguardar(" Função atualizada com sucesso!")
            elif escolha == "2":
                self.usuario_logado.funcao = "Técnico"
                self.gerenciador.atualizar_usuario(self.usuario_logado.email, self.usuario_logado)
                Interface.exibir_e_aguardar(" Função atualizada com sucesso!")
            else:
                Interface.exibir_e_aguardar(" Opção inválida!")
        
        elif opcao == "0":
            Interface.exibir_e_aguardar("Voltando ao menu...")
            return
        
        else:
            Interface.exibir_e_aguardar(" Opção inválida!")
    
    def excluir_conta(self):
        """Permite ao usuário logado excluir sua conta"""
        if self.usuario_logado is None:
            print("Nenhum usuário logado!")
            return False
        
        print("\n" + "_" * 50)
        print("EXCLUIR CONTA")
        print("_" * 50)
        confirmacao = input("\nTem certeza que deseja excluir sua conta? (S/N): ").strip().upper()
        
        if confirmacao == "S":
            self.gerenciador.deletar_usuario(self.usuario_logado.email)
            Interface.exibir_e_aguardar(" Sua conta foi excluída com sucesso!\nVoltando ao menu principal...", 2.0)
            self.usuario_logado = None
            return True
        else:
            Interface.exibir_e_aguardar("Exclusão cancelada!")
            return False
