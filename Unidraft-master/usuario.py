import json
import os


class Usuario:
   
    
    def __init__(self, nome, email, senha, modalidade, funcao):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.modalidade = modalidade
        self.funcao = funcao
        self.esporte = ""
    
    def to_dict(self):
        
        return {
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "esporte": self.esporte,
            "modalidade": self.modalidade,
            "funcao": self.funcao
        }
    
    @staticmethod
    def from_dict(dados):
      
        usuario = Usuario(
            dados["nome"],
            dados["email"],
            dados["senha"],
            dados["modalidade"],
            dados["funcao"]
        )
        usuario.esporte = dados.get("esporte", "")
        return usuario


class GerenciadorUsuarios:
   
    
    def __init__(self, arquivo="usuarios.json"):
        self.arquivo = arquivo
    
    def carregar_usuarios(self):
       
        if not os.path.exists(self.arquivo) or os.path.getsize(self.arquivo) == 0:
            return []
        with open(self.arquivo, "r") as f:
            return json.load(f)
    
    def salvar_usuarios(self, usuarios_dict):
        
        with open(self.arquivo, "w") as f:
            json.dump(usuarios_dict, f, indent=4)
    
    def adicionar_usuario(self, usuario):
       
        usuarios = self.carregar_usuarios()
        usuarios.append(usuario.to_dict())
        self.salvar_usuarios(usuarios)
    
    def obter_usuario(self, email):
        
        usuarios = self.carregar_usuarios()
        for dados in usuarios:
            if dados["email"] == email:
                return Usuario.from_dict(dados)
        return None
    
    def atualizar_usuario(self, email, usuario):
        
        usuarios = self.carregar_usuarios()
        for u in usuarios:
            if u["email"] == email:
                u.update(usuario.to_dict())
                break
        self.salvar_usuarios(usuarios)
    
    def deletar_usuario(self, email):
        
        usuarios = self.carregar_usuarios()
        usuarios = [u for u in usuarios if u["email"] != email]
        self.salvar_usuarios(usuarios)
    
    def usuario_existe(self, email):
        
        return self.obter_usuario(email) is not None
