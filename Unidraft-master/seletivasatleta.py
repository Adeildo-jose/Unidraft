import json
import os
from interface import Interface
from email_utils import send_registration_email, send_cancellation_email, send_seletiva_canceled_email


class GerenciadorSeletivas:

    def __init__(self, arquivo="seletivas.json"):
        self.arquivo = arquivo

    def carregar_seletivas(self):
        if not os.path.exists(self.arquivo) or os.path.getsize(self.arquivo) == 0:
            return []
        with open(self.arquivo, "r", encoding="utf-8") as f:
            return json.load(f)

    def salvar_seletivas(self, seletivas):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(seletivas, f, indent=4, ensure_ascii=False)

    def gerar_id(self, seletivas):
        if len(seletivas) == 0:
            return 1
        return seletivas[-1]["id"] + 1


class MenuTreinador:

    def __init__(self, email_treinador, esporte_treinador):
        self.email = email_treinador
        self.esporte = esporte_treinador
        self.gerenciador = GerenciadorSeletivas()

    def criar_seletiva(self):
        Interface.limpar_tela()
        print("_" * 50)
        print("CRIAR SELETIVA\n")
        print("_" * 50)

        if not self.esporte:
            Interface.exibir_e_aguardar("Você precisa marcar um esporte no seu perfil antes de criar uma seletiva.")
            return

        print(f"Esporte da seletiva: {self.esporte}\n")

        while True:
            data = input("Digite a data e horário (ex: 10/06/2025 às 14h): ").strip()
            if data == "":
                print("A data não pode ser vazia. Tente novamente.\n")
            else:
                break

        while True:
            limite_texto = input("Digite o limite de participantes: ").strip()
            if not limite_texto.isdigit():
                print("Digite apenas números. Tente novamente.\n")
                continue
            limite = int(limite_texto)
            if limite <= 0:
                print("O limite deve ser maior que zero. Tente novamente.\n")
            else:
                break

        seletivas = self.gerenciador.carregar_seletivas()
        novo_id = self.gerenciador.gerar_id(seletivas)

        seletivas.append({
            "id": novo_id,
            "esporte": self.esporte,
            "data": data,
            "limite": limite,
            "inscritos": [],
            "email_treinador": self.email
        })

        self.gerenciador.salvar_seletivas(seletivas)
        Interface.exibir_e_aguardar(f"\nSeletiva criada com sucesso! (ID: {novo_id})")

    def cancelar_seletiva(self):
        Interface.limpar_tela()
        print("_" * 50)
        print("CANCELAR SELETIVA\n")
        print("_" * 50)

        seletivas = self.gerenciador.carregar_seletivas()

        minhas_seletivas = []
        for s in seletivas:
            if s["email_treinador"] == self.email:
                minhas_seletivas.append(s)

        if len(minhas_seletivas) == 0:
            Interface.exibir_e_aguardar("Você não criou nenhuma seletiva ainda.")
            return

        print("Suas seletivas:\n")
        for s in minhas_seletivas:
            print(f"ID: {s['id']} | Esporte: {s['esporte']} | Data: {s['data']} | Inscritos: {len(s['inscritos'])}")

        print()

        while True:
            id_texto = input("Digite o ID da seletiva para cancelar (0 para voltar): ").strip()
            if id_texto == "0":
                return
            if not id_texto.isdigit():
                print("Digite apenas números. Tente novamente.\n")
                continue

            id_escolhido = int(id_texto)

            ids_existentes = []
            for s in minhas_seletivas:
                ids_existentes.append(s["id"])

            if id_escolhido not in ids_existentes:
                print("ID inválido. Tente novamente.\n")
            else:
                break

        confirmacao = input(f"\nTem certeza que deseja cancelar a seletiva ID {id_escolhido}? (s/n): ").strip().lower()
        if confirmacao != "s":
            Interface.exibir_e_aguardar("Cancelamento abortado.")
            return

        indice = None
        for i in range(len(seletivas)):
            if seletivas[i]["id"] == id_escolhido:
                indice = i
                break

        seletiva_removida = seletivas.pop(indice)
        self.gerenciador.salvar_seletivas(seletivas)

        inscritos = seletiva_removida.get("inscritos", [])
        if inscritos:
            try:
                send_seletiva_canceled_email(inscritos, seletiva_removida)
            except Exception as e:
                print(f"Erro ao notificar inscritos: {e}")

        Interface.exibir_e_aguardar(f"\nSeletiva ID {id_escolhido} cancelada com sucesso!")

    def ver_inscritos(self):
        Interface.limpar_tela()
        print("_" * 50)
        print("MINHAS SELETIVAS\n")
        print("_" * 50)

        seletivas = self.gerenciador.carregar_seletivas()

        minhas_seletivas = []
        for s in seletivas:
            if s["email_treinador"] == self.email:
                minhas_seletivas.append(s)

        if len(minhas_seletivas) == 0:
            Interface.exibir_e_aguardar("Você ainda não criou nenhuma seletiva.")
            return

        for s in minhas_seletivas:
            vagas_restantes = s["limite"] - len(s["inscritos"])
            print(f"\nID: {s['id']} | Esporte: {s['esporte']} | Data: {s['data']}")
            print(f"Vagas: {len(s['inscritos'])}/{s['limite']} preenchidas | Restam: {vagas_restantes}")

            if len(s["inscritos"]) == 0:
                print("Inscritos: nenhum até o momento.")
            else:
                print("Inscritos:")
                for email in s["inscritos"]:
                    print(f"  - {email}")

        Interface.pausa_com_clear()

    def executar_menu(self):
        while True:
            Interface.limpar_tela()
            print("_" * 50)
            print("MENU DO TREINADOR\n")
            print("_" * 50)
            print("\n[1] Criar seletiva")
            print("[2] Ver inscritos nas minhas seletivas")
            print("[3] Cancelar seletiva")
            print("[0] Voltar\n")

            escolha = input("Escolha uma opção: ").strip()

            if escolha == "1":
                self.criar_seletiva()
            elif escolha == "2":
                self.ver_inscritos()
            elif escolha == "3":
                self.cancelar_seletiva()
            elif escolha == "0":
                break
            else:
                Interface.exibir_e_aguardar("Opção inválida. Tente novamente.")


class MenuAtleta:

    def __init__(self, email_atleta, esporte_atleta):
        self.email = email_atleta
        self.esporte = esporte_atleta
        self.gerenciador = GerenciadorSeletivas()

    def ver_seletivas_disponiveis(self):
        Interface.limpar_tela()
        print("_" * 50)
        print("SELETIVAS DISPONÍVEIS\n")
        print("_" * 50)

        if not self.esporte:
            Interface.exibir_e_aguardar("Você precisa marcar um esporte no seu perfil para ver as seletivas.")
            return

        seletivas = self.gerenciador.carregar_seletivas()

        disponiveis = []
        for s in seletivas:
            if s["esporte"] == self.esporte:
                disponiveis.append(s)

        if len(disponiveis) == 0:
            Interface.exibir_e_aguardar(f"Nenhuma seletiva disponível para {self.esporte} no momento.")
            return

        for s in disponiveis:
            vagas_restantes = s["limite"] - len(s["inscritos"])
            inscrito = self.email in s["inscritos"]

            print(f"\nID: {s['id']} | Esporte: {s['esporte']} | Data: {s['data']}")
            print(f"Vagas restantes: {vagas_restantes}/{s['limite']}")

            if inscrito:
                print("Situação: você está inscrito nesta seletiva.")
            elif vagas_restantes == 0:
                print("Situação: seletiva lotada.")
            else:
                print("Situação: vaga disponível.")

        Interface.pausa_com_clear()

    def inscrever_em_seletiva(self):
        Interface.limpar_tela()
        print("_" * 50)
        print("INSCREVER-SE EM SELETIVA\n")
        print("_" * 50)

        if not self.esporte:
            Interface.exibir_e_aguardar("Você precisa marcar um esporte no seu perfil antes de se inscrever.")
            return

        seletivas = self.gerenciador.carregar_seletivas()

        disponiveis = []
        for s in seletivas:
            if s["esporte"] == self.esporte:
                disponiveis.append(s)

        if len(disponiveis) == 0:
            Interface.exibir_e_aguardar(f"Nenhuma seletiva disponível para {self.esporte} no momento.")
            return

        for s in disponiveis:
            vagas_restantes = s["limite"] - len(s["inscritos"])
            inscrito = self.email in s["inscritos"]
            print(f"\nID: {s['id']} | Data: {s['data']} | Vagas restantes: {vagas_restantes}", end="")
            if inscrito:
                print(" | JÁ INSCRITO", end="")
            print()

        print()

        while True:
            id_texto = input("Digite o ID da seletiva (0 para voltar): ").strip()
            if id_texto == "0":
                return
            if not id_texto.isdigit():
                print("Digite apenas números. Tente novamente.\n")
                continue

            id_escolhido = int(id_texto)

            ids_disponiveis = []
            for s in disponiveis:
                ids_disponiveis.append(s["id"])

            if id_escolhido not in ids_disponiveis:
                print("ID inválido. Tente novamente.\n")
            else:
                break

        indice = None
        for i in range(len(seletivas)):
            if seletivas[i]["id"] == id_escolhido:
                indice = i
                break

        seletiva = seletivas[indice]

        if self.email in seletiva["inscritos"]:
            Interface.exibir_e_aguardar("Você já está inscrito nesta seletiva.")
            return

        vagas_restantes = seletiva["limite"] - len(seletiva["inscritos"])
        if vagas_restantes == 0:
            Interface.exibir_e_aguardar("Esta seletiva está lotada. Não foi possível se inscrever.")
            return

        seletiva["inscritos"].append(self.email)
        seletivas[indice] = seletiva
        self.gerenciador.salvar_seletivas(seletivas)

        treinador_email = seletiva.get("email_treinador", "")
        enviado = False
        try:
            enviado = send_registration_email(treinador_email, self.email, seletiva)
        except Exception as e:
            print("Erro ao tentar enviar e-mail:", e)

        if enviado:
            Interface.exibir_e_aguardar(f"\nInscrição realizada com sucesso! Até dia {seletiva['data']}.\nE-mail enviado ao treinador.")
        else:
            Interface.exibir_e_aguardar(f"\nInscrição realizada com sucesso! Até dia {seletiva['data']}.\nNão foi possível enviar o e-mail ao treinador.")

    def cancelar_inscricao(self):
        Interface.limpar_tela()
        print("_" * 50)
        print("CANCELAR INSCRIÇÃO\n")
        print("_" * 50)

        seletivas = self.gerenciador.carregar_seletivas()

        minhas_inscricoes = []
        for s in seletivas:
            if self.email in s["inscritos"]:
                minhas_inscricoes.append(s)

        if len(minhas_inscricoes) == 0:
            Interface.exibir_e_aguardar("Você não está inscrito em nenhuma seletiva.")
            return

        print("Suas inscrições:\n")
        for s in minhas_inscricoes:
            print(f"ID: {s['id']} | Esporte: {s['esporte']} | Data: {s['data']}")

        print()

        while True:
            id_texto = input("Digite o ID que deseja cancelar (0 para voltar): ").strip()
            if id_texto == "0":
                return
            if not id_texto.isdigit():
                print("Digite apenas números. Tente novamente.\n")
                continue

            id_escolhido = int(id_texto)

            ids_inscritos = []
            for s in minhas_inscricoes:
                ids_inscritos.append(s["id"])

            if id_escolhido not in ids_inscritos:
                print("ID inválido. Tente novamente.\n")
            else:
                break

        for i in range(len(seletivas)):
            if seletivas[i]["id"] == id_escolhido:
                seletiva = seletivas[i]
                seletiva["inscritos"].remove(self.email)
                self.gerenciador.salvar_seletivas(seletivas)

                treinador_email = seletiva.get("email_treinador", "")
                enviado = False
                try:
                    enviado = send_cancellation_email(treinador_email, self.email, seletiva)
                except Exception as e:
                    print("Erro ao tentar enviar e-mail:", e)

                if enviado:
                    Interface.exibir_e_aguardar("\nInscrição cancelada com sucesso. E-mail enviado ao treinador.")
                else:
                    Interface.exibir_e_aguardar("\nInscrição cancelada com sucesso. Não foi possível enviar o e-mail ao treinador.")
                return

    def executar_menu(self):
        while True:
            Interface.limpar_tela()
            print("_" * 50)
            print("MENU DO ATLETA\n")
            print("_" * 50)
            print("\n[1] Ver seletivas disponíveis")
            print("[2] Inscrever-se em seletiva")
            print("[3] Cancelar inscrição em seletiva")
            print("[0] Voltar\n")

            escolha = input("Escolha uma opção: ").strip()

            if escolha == "1":
                self.ver_seletivas_disponiveis()
            elif escolha == "2":
                self.inscrever_em_seletiva()
            elif escolha == "3":
                self.cancelar_inscricao()
            elif escolha == "0":
                break
            else:
                Interface.exibir_e_aguardar("Opção inválida. Tente novamente.")
