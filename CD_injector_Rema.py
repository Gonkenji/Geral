import pandas as pd
import re
import os

def atualizar_config_h():
    path_base = r'C:\Users\proje\OneDrive\Documentos\Gon'
    caminho_xlsx = os.path.join(path_base, 'dados.xlsx')
    caminho_h = os.path.join(path_base, 'config.h')
    caminho_saida = os.path.join(path_base, 'config_Stock14.h')

    if not os.path.exists(caminho_xlsx):
        print(f"Erro: Arquivo {caminho_xlsx} nao encontrado.")
        return

    try:
        df = pd.read_excel(caminho_xlsx, header=None)
    except:
        df = pd.read_csv(caminho_xlsx, header=None)

    mapping_data = {}
    for _, row in df.iterrows():
        linha = str(row[0]).replace('"', '').strip().rstrip(',')
        if ':' in linha:
            key, val = linha.split(':')
            mapping_data[key.strip()] = val.strip()

    name_map = {
        "tempH1NId": "T1N", "tempH1SId": "T1S", "tempH1EId": "T1E", "tempH1WId": "T1W",
        "tempH2NId": "T2N", "tempH2SId": "T2S", "tempH2EId": "T2E", "tempH2WId": "T2W",
        "tempH3NId": "T3N", "tempH3SId": "T3S", "tempH3EId": "T3E", "tempH3WId": "T3W",
        "tempTop2": "T2top", "tempTop3": "T3top", "tempBtm2": "T2btm", "tempBtm3": "T3btm",
        "humH1Id": "H1", "humH2Id": "H2", "humH3Id": "H3",
        "tempExtId": "tempExt", "humExtId": "humExt",
        "waterLevelId": "waterLevel", "batteryVoltId": "batteryVolt"
    }

    with open(caminho_h, 'r', encoding='utf-8') as f:
        content = f.read()

    for csv_key, json_name in name_map.items():
        if csv_key in mapping_data:
            novo_id = mapping_data[csv_key]

            padrao = rf'("name":"{json_name}".*?"cd":)(\d+)'

            content = re.sub(padrao, rf'\g<1>{novo_id}', content, flags=re.DOTALL)

    with open(caminho_saida, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

    print("IDs atualizados")

if __name__ == "__main__":
    atualizar_config_h()
