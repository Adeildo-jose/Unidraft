import re
from usuario import Usuario, GerenciadorUsuarios
from interface import Interface


class ValidadorDados:
    
    
    PADRAO_EMAIL = r'^[a-zA-Z]+\.[a-zA-Z]+@ufrpe\.br$'
    TAM_MIN_NOME = 3
    TAM_MAX_NOME = 100
    TAM_MIN_SENHA = 6
    
    @staticmethod
    def validar_nome(nome):
       
        nome = nome.strip()
        if not nome:
            return False, "O nome não pode ser vazio."
        if not nome.replace(" ", "").isalpha():
            return False, "O nome só pode conter letras."
        if len(nome) < ValidadorDados.TAM_MIN_NOME:
            return False, f"O nome deve ter no mínimo {ValidadorDados.TAM_MIN_NOME} caracteres."
        if len(nome) > ValidadorDados.TAM_MAX_NOME:
            return False, f"O nome deve ter no máximo {ValidadorDados.TAM_MAX_NOME} caracteres."
        return True, "OK"
    
    @staticmethod
    def validar_email(email):
       
        email = email.strip()
        if not email:
            return False, "O email não pode ser vazio."
        if not re.match(ValidadorDados.PADRAO_EMAIL, email):
            return False, "Email inválido. Use formato: nome.sobrenome@ufrpe.br"
        return True, "OK"
    
    @staticmethod
    def validar_senha(senha):
      
        if not senha:
            return False, "A senha não pode ser vazia."
        if len(senha) < ValidadorDados.TAM_MIN_SENHA:
            return False, f"A senha deve ter pelo menos {ValidadorDados.TAM_MIN_SENHA} caracteres."
        return True, "OK"


class Cadastro:
    
    
    def __init__(self):
        self.gerenciador = GerenciadorUsuarios()
        self.validador = ValidadorDados()
    
    def pedir_nome(self):
        
        while True:
            nome = input("Digite seu nome: ")
            valido, mensagem = self.validador.validar_nome(nome)
            if valido:
                return nome.strip()
            print(f"{mensagem}\n")
    
    def pedir_email(self):
        
        while True:
            email = input("Digite seu email: ")
            valido, mensagem = self.validador.validar_email(email)
            if not valido:
                print(f"{mensagem}\n")
                continue
            if self.gerenciador.usuario_existe(email.strip()):
                print("Este email já está cadastrado.\n")
                continue
            return email.strip()
    
    def pedir_senha(self):
        
        while True:
            senha = input("Digite sua senha: ")
            valido, mensagem = self.validador.validar_senha(senha)
            if valido:
                return senha
            print(f"{mensagem}\n")
    
    def pedir_modalidade(self):
        
        while True:
            print("Selecione sua modalidade:")
            print("[1] Masculino")
            print("[2] Feminino")
            print("[0] voltar\n")
            escolha = input("Escolha uma opção: ")
            
            if escolha == "1":
                return "Masculino"
            elif escolha == "2":
                return "Feminino"
            elif escolha == "0":
                return None
            else:
                print("Opção inválida. Tente novamente.\n")
    
    def pedir_funcao(self):
        
        while True:
            print("Escolha sua função:")
            print("[1] Atleta")
            print("[2] Técnico")
            print("[0] voltar\n")
            escolha = input("Escolha uma opção: ")
            
            if escolha == "1":
                return "Atleta"
            elif escolha == "2":
                return "Técnico"
            elif escolha == "0":
                return None
            else:
                print("Opção inválida. Tente novamente.\n")
    
    def fazer_cadastro(self):
        
        print("_" * 50)
        print("FAÇA SEU CADASTRO\n")
        print("_" * 50)
        
        nome = self.pedir_nome()
        
        while True:
            email = self.pedir_email()
            senha = self.pedir_senha()
            modalidade = self.pedir_modalidade()
            
            if modalidade is None:
                continue
            
            funcao = self.pedir_funcao()
            
            if funcao is None:
                continue
            
            # Criar novo usuário e salvar
            novo_usuario = Usuario(nome, email, senha, modalidade, funcao)
            self.gerenciador.adicionar_usuario(novo_usuario)
            
            Interface.exibir_e_aguardar("\n✓ Cadastro realizado com sucesso!")
            break
