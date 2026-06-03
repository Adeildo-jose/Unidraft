import os
import time


class Interface:
    
    TEMPO_ESPERA = 1  
    
    @staticmethod
    def limpar_tela():

        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def aguardar_com_clear(tempo=None):
       
        if tempo is None:
            tempo = Interface.TEMPO_ESPERA
        time.sleep(tempo)
        Interface.limpar_tela()
    
    @staticmethod
    def exibir_e_aguardar(mensagem, tempo=None):
        
        print(mensagem)
        Interface.aguardar_com_clear(tempo)
    
    @staticmethod
    def pausa_com_clear():
       
        input("\nPressione ENTER para continuar...")
        Interface.limpar_tela()
