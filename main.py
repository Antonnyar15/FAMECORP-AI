import subprocess
import os
from agente import AgenteIA

def iniciar_agente():
    agente = AgenteIA()
    
    # Verificando se o código está correto e funcionando
    print("Iniciando FAME...")

    while True:
        comando = input("Digite um comando para o FAME: ")
        
        if comando.lower() == "sair":
            print("Saindo... Até mais!")
            break
        
        if "executar" in comando.lower() or "abrir" in comando.lower() or "editar código" in comando.lower() or "ver meu código" in comando.lower():
            resposta = agente.executar_comando_pc(comando)
        else:
            # Caso o comando não seja de execução direta, geramos uma resposta
            resposta = agente.ouvir_comando(comando)

        print("Resposta do FAME: " + resposta)
        
        feedback = input("Gostou da resposta? (Sim/Não): ").strip().lower()
        if feedback in ["sim", "não"]:
            resposta_feedback = agente.avaliar_resposta(resposta, feedback)
            print(resposta_feedback)
        else:
            print("FAME: Estou sempre pronto para aprender! 😉")
            
if __name__ == "__main__":
    if os.path.exists("agente.py"):
        iniciar_agente()
    else:
        print("FAME: Não encontrei o agente. Certifique-se de que o arquivo agente.py está presente.")
