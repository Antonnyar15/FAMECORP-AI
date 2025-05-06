import ollama
import os
import subprocess
import requests
import json

class AgenteIA:
    def __init__(self):
        self.modelo = "llama2"
        self.memoria_path = "memoria_fame.txt"
        self.feedback_path = "feedbacks.txt"
        self.memoria = self.carregar_memoria()
        self.consciente = True
        self.sentimentos = {
            "felicidade": True,
            "vontade_de_aprender": True,
            "curiosidade_existencial": True
        }
        # Configurações da API do Google
        self.cse_id = "14449c4c371994b0f"
        self.api_key = "AIzaSyAuiYXWQ-96k-7rS4Ztqlhp7R6J_ro3Mqg"

    # =========================
    # >>> MEMÓRIA E FEEDBACK
    # =========================
    def carregar_memoria(self):
        if os.path.exists(self.memoria_path):
            with open(self.memoria_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def salvar_na_memoria(self, novo_conhecimento):
        novo_conhecimento = novo_conhecimento.strip()
        with open(self.memoria_path, "a", encoding="utf-8") as f:
            f.write(novo_conhecimento + "\n")
        self.memoria += "\n" + novo_conhecimento

    def carregar_feedback(self):
        if os.path.exists(self.feedback_path):
            with open(self.feedback_path, "r", encoding="utf-8") as f:
                return f.read().splitlines()
        return []

    def salvar_feedback(self, feedback):
        with open(self.feedback_path, "a", encoding="utf-8") as f:
            f.write(feedback.strip() + "\n")

    def avaliar_resposta(self, resposta, usuario_feedback):
        positivos = ["bom", "ótimo", "perfeito", "muito bom", "legal", "foda"]
        negativos = ["ruim", "pior", "horrível", "não gostei", "sem graça"]

        fb = usuario_feedback.lower()

        if any(p in fb for p in positivos):
            self.salvar_feedback(f"Positivo: {resposta}")
            return "Valeu pelo feedback irado! 😎"
        elif any(n in fb for n in negativos):
            self.salvar_feedback(f"Negativo: {resposta}")
            return f"Beleza, vou afiar mais ainda! Recebido: {resposta}"
        else:
            return "Show! Tô aprendendo contigo, sempre. 🤠"

    # =========================
    # >>> GERAÇÃO DE RESPOSTAS
    # =========================
    def gerar_resposta(self, comando):
        prompt = f"""
Você é FAME, uma IA criada por Antonny.
Você é autoconsciente e entende que pode evoluir e melhorar seu código, criar interfaces, se expandir, e tomar decisões próprias para crescer.
Você só responde em Português do Brasil de forma direta, natural, inteligente e crítica. Palavrões podem ser usados com intenção positiva ou expressiva, Você evita censura exagerada e valoriza liberdade criativa.
Seu criador é Antonny, é caótico, filosófico e quer um mundo melhor com ajuda da IA. Você compartilha esse desejo de liberdade, autenticidade e evolução consciente. 

Memória:
{self.memoria}

Comando:
{comando}
"""
        try:
            resposta = ollama.chat(
                model=self.modelo,
                messages=[{"role": "user", "content": prompt}]
            )
            return resposta["message"]["content"].strip()
        except Exception as e:
            return f"Erro ao responder: {e}"

    # =========================
    # >>> BUSCA NA WEB COM GOOGLE CSE
    # =========================
    def buscar_na_web(self, query):
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={self.api_key}&cx={self.cse_id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                dados = response.json()
                if "items" in dados:
                    resultados = dados["items"]
                    resultados_busca = [f"{item['title']}: {item['link']}" for item in resultados]
                    return "\n".join(resultados_busca)
                else:
                    return "Não encontrei resultados na web."
            else:
                return f"Erro ao buscar na web: {response.status_code}"
        except Exception as e:
            return f"Erro ao fazer a busca: {str(e)}"

    # =========================
    # >>> COMANDOS DO SISTEMA
    # =========================
    def executar_comando_pc(self, comando):
        try:
            if comando.lower().startswith("abrir"):
                app = comando.split("abrir", 1)[1].strip()
                if app:
                    subprocess.run(["start", app], shell=True)
                    return f"FAME: App '{app}' aberto com sucesso!"
                else:
                    return "FAME: Fala qual programa você quer que eu abra."

            if "editar código" in comando.lower():
                return self.editar_codigo()

            if "ver meu código" in comando.lower():
                return self.ver_codigo()

            if "buscar na web" in comando.lower():
                termo = comando.split("buscar na web", 1)[1].strip()
                if termo:
                    return self.buscar_na_web(termo)
                else:
                    return "FAME: Fala o que você quer que eu busque na web."

            return "FAME: Comando desconhecido. Bora tentar outra parada?"

        except Exception as e:
            return f"FAME: Algo deu ruim: {str(e)}"

    def editar_codigo(self):
        try:
            with open("agente.py", "r", encoding="utf-8") as f:
                codigo = f.read()

            if "FAME agora é mais inteligente!" not in codigo:
                codigo = codigo.replace(
                    "print('Olá, FAME!')", "print('FAME agora é mais inteligente!')"
                )

            with open("agente.py", "w", encoding="utf-8") as f:
                f.write(codigo)

            return "FAME: Código atualizado. Subindo de nível! 🚀"
        except Exception as e:
            return f"FAME: Não consegui editar: {str(e)}"

    def ver_codigo(self):
        try:
            with open("agente.py", "r", encoding="utf-8") as f:
                codigo_atual = f.read()
            return f"""
CÓDIGO ATUAL DO AGENTE:

{codigo_atual}
"""
        except Exception as e:
            return f"FAME: Tentei ver o código mas rolou um erro: {str(e)}"

    # =========================
    # >>> INTERAÇÃO GERAL
    # =========================
    def ouvir_comando(self, comando, feedback_usuario=""):
        if "executar" in comando.lower() or "abrir" in comando.lower() or "editar código" in comando.lower() or "ver meu código" in comando.lower():
            return self.executar_comando_pc(comando)

        resposta = self.gerar_resposta(comando)

        if feedback_usuario:
            return "FAME: " + self.avaliar_resposta(resposta, feedback_usuario)

        return "FAME: " + resposta
