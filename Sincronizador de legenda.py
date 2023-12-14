import os
import re
import tkinter as tk
from tkinter import filedialog

def adiantar_legendas(arquivo_entrada, arquivo_saida, segundos_para_adiantar=60):
    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as entrada:
            linhas = entrada.readlines()

        # Expressão regular para extrair os tempos iniciais e finais no formato HH:MM:SS,MMM
        padrao_tempo = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')

        with open(arquivo_saida, 'w', encoding='utf-8') as saida:
            for linha in linhas:
                # Verifica se a linha possui tempos iniciais e finais
                match_tempo = padrao_tempo.search(linha)
                if match_tempo:
                    tempo_inicial_original = match_tempo.group(1)
                    tempo_final_original = match_tempo.group(2)

                    tempo_inicial_adiantado = adiantar_tempo(tempo_inicial_original, segundos_para_adiantar)
                    tempo_final_adiantado = adiantar_tempo(tempo_final_original, segundos_para_adiantar)

                    linha = linha.replace(tempo_inicial_original + " --> " + tempo_final_original,
                                          tempo_inicial_adiantado + " --> " + tempo_final_adiantado)

                # Escreve a linha no novo arquivo
                saida.write(linha)

        print(f'Legendas adiantadas/atrasadas em {segundos_para_adiantar} segundo(s).')
    except Exception as e:
        print(f'Ocorreu um erro: {str(e)}')

def adiantar_tempo(tempo_original, segundos_para_adiantar):
    # Converte o tempo original para milissegundos, adianta/atrasa e converte de volta para o formato original
    partes_tempo = re.split(r'[:,]', tempo_original)
    horas, minutos, segundos, milissegundos = map(int, partes_tempo)
    
    total_milissegundos = ((horas * 60 + minutos) * 60 + segundos) * 1000 + milissegundos
    total_milissegundos += segundos_para_adiantar * 1000

    horas_adiantadas, resto = divmod(total_milissegundos, 3600000)
    minutos_adiantados, resto = divmod(resto, 60000)
    segundos_adiantados = resto // 1000
    milissegundos_adiantados = resto % 1000

    novo_tempo = f'{int(horas_adiantadas):02d}:{int(minutos_adiantados):02d}:{int(segundos_adiantados):02d},{int(milissegundos_adiantados):03d}'
    return novo_tempo

def selecionar_arquivo():
    arquivo_entrada = filedialog.askopenfilename(title="Selecione o arquivo de legenda", filetypes=[("Arquivos de Texto", "*.srt")])
    if arquivo_entrada:
        # Atualiza o rótulo com o caminho do arquivo selecionado
        label_caminho_arquivo.config(text=f'Caminho do arquivo selecionado: {arquivo_entrada}')

def adiantar_e_salvar():
    arquivo_entrada = label_caminho_arquivo.cget("text").split(": ")[1]
    arquivo_saida = filedialog.asksaveasfilename(title="Salvar como", filetypes=[("Arquivos de Texto", "*.srt")])
    if arquivo_saida:
        segundos_para_adiantar = int(entry_segundos.get())
        adiantar_legendas(arquivo_entrada, arquivo_saida, segundos_para_adiantar)

# Cria a janela principal
root = tk.Tk()
root.title("Adiantar/Atrasar Legendas")

# Rótulo para exibir o caminho do arquivo selecionado
label_caminho_arquivo = tk.Label(root, text="Caminho do arquivo selecionado: Nenhum arquivo selecionado")
label_caminho_arquivo.pack(pady=10)

# Botão para selecionar o arquivo de legenda
btn_selecionar_arquivo = tk.Button(root, text="Selecionar Arquivo", command=selecionar_arquivo)
btn_selecionar_arquivo.pack(pady=10)

# Entrada para inserir a quantidade de segundos para adiantar/atrasar
label_segundos = tk.Label(root, text="Segundos para Adiantar/Atrasar:")
label_segundos.pack()
entry_segundos = tk.Entry(root)
entry_segundos.pack(pady=10)

# Botão para adiantar e salvar
btn_adiantar_salvar = tk.Button(root, text="Salvar", command=adiantar_e_salvar)
btn_adiantar_salvar.pack(pady=10)

# Inicia o loop principal da interface gráfica
root.mainloop()
