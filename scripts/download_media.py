"""Download PDFs and videos from DI links into each module's media folder."""
import os, re, requests, time, json
from pathlib import Path
from urllib.parse import urlparse

BASE = Path(r"c:\Users\AparicioJunior\workspace\saude-caminhoneiros")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/pdf,*/*",
}

PDFS = {
    1: [
        ("politica_nacional_promocao_saude.pdf",
         "https://bvsms.saude.gov.br/bvs/publicacoes/politica_nacional_promocao_saude.pdf"),
        ("livro_conass_vigilancia.pdf",
         "http://www.conass.org.br/bibliotecav3/pdfs/colecao2011/livro_5.pdf"),
        ("saude_caminhoneiros_editoracientifica.pdf",
         "https://downloads.editoracientifica.com.br/articles/220308367.pdf"),
        ("politica_nacional_atencao_saude_homem.pdf",
         "https://bvsms.saude.gov.br/bvs/publicacoes/politica_nacional_atencao_saude_homem.pdf"),
        ("politica_nac_atencao_mulher.pdf",
         "https://bvsms.saude.gov.br/bvs/publicacoes/politica_nac_atencao_mulher.pdf"),
        ("pnps_revisao_portaria_687.pdf",
         "https://bvsms.saude.gov.br/bvs/publicacoes/pnps_revisao_portaria_687.pdf"),
        ("freitas_riscos_ambientais.pdf",
         "http://www.scielo.br/pdf/csc/v23n6/1413-8123-csc-23-06-1981.pdf"),
        ("acolhimento_demanda_espontanea_cab28.pdf",
         "https://bvsms.saude.gov.br/bvs/publicacoes/acolhimento_demanda_espontanea_queixas_comuns_cab28v2.pdf"),
        ("starfield_atencao_primaria.pdf",
         "http://www.dominiopublico.gov.br/download/texto/ue000039.pdf"),
    ],
    2: [
        ("pcdt_prep_hiv.pdf",
         "http://www.gov.br/aids/pt-br/central-de-conteudo/pcdts/protocolo-clinico-e-diretrizes-terapeuticas-para-profilaxia-pre-exposicao-prep-oral-a-infeccao-pelo-hiv.pdf/@@display-file/file"),
        ("calendario_vacinacao_2026.pdf",
         "https://www.gov.br/saude/pt-br/vacinacao/publicacoes/instrucao-normativa-que-instrui-o-calendario-nacional-de-vacinacao-2026.pdf"),
        ("pcdt_ist_2022.pdf",
         "http://www.gov.br/aids/pt-br/central-de-conteudo/pcdts/2022/ist/pcdt-ist-2022_isbn-1.pdf"),
        ("pcdt_pep_hiv_2021.pdf",
         "http://www.gov.br/aids/pt-br/central-de-conteudo/pcdts/2021/hiv-aids/prot_clinico_diretrizes_terap_pep_-risco_infeccao_hiv_ist_hv_2021.pdf/@@display-file/file"),
        ("rowley_chlamydia_gonorrhea_BLT.pdf",
         "https://pmc.ncbi.nlm.nih.gov/articles/PMC6653813/pdf/BLT.18.228486.pdf"),
        ("manual_imunobiologicos_6ed.pdf",
         "http://bvsms.saude.gov.br/bvs/publicacoes/manual_centros_referencia_imunobiologicos_6ed.pdf"),
        ("guia_vigilancia_saude.pdf",
         "https://bvsms.saude.gov.br/bvs/publicacoes/guia_vigilancia_saude_v2_6edrev.pdf"),
        ("pcdt_hiv_modulo1_2024.pdf",
         "http://www.gov.br/aids/pt-br/central-de-conteudo/pcdts/pcdt_hiv_modulo_1_2024.pdf"),
        ("sei_nota_distribuicao_preservativos.pdf",
         "https://egestorab.saude.gov.br/image/?file=20210430_N_SEI25000.156178202097_1396110966499381938.pdf"),
    ],
    3: [
        ("DSM-V.pdf",
         "https://membros.analysispsicologia.com.br/wp-content/uploads/2024/06/DSM-V.pdf"),
    ],
    4: [
        ("plano_dant_2022_2030.pdf",
         "https://www.gov.br/saude/pt-br/centrais-de-conteudo/publicacoes/svsa/doencas-cronicas-nao-transmissiveis-dcnt/09-plano-de-dant-2022_2030.pdf"),
        ("diretriz_has_sbc_2020.pdf",
         "http://departamentos.cardiol.br/sbc-dha/profissional/pdf/Diretriz-HAS-2020.pdf"),
    ],
    5: [
        ("manual_prevencao_suicidio_saude.pdf",
         "https://cvv.org.br/wp-content/uploads/2023/08/manual_prevencao_suicidio_profissionais_saude.pdf"),
        ("cuidado_saude_homem_violencia.pdf",
         "http://bvsms.saude.gov.br/bvs/publicacoes/cuidado_saude_homem_contexto_violencia.pdf"),
        ("vasconcelos_genero_masculinidades.pdf",
         "https://pdfs.semanticscholar.org/1e17/6ee6cc7d10bb993553e11ec9bfcc3c27a474.pdf"),
    ],
}

results = {}

for mod, items in PDFS.items():
    dest_dir = BASE / f"modulo {mod}" / "media"
    dest_dir.mkdir(exist_ok=True)
    results[mod] = []
    for fname, url in items:
        dest = dest_dir / fname
        if dest.exists() and dest.stat().st_size > 1024:
            print(f"[SKIP] {fname} already exists")
            results[mod].append({"file": fname, "url": url, "status": "exists"})
            continue
        try:
            print(f"[DL]  {fname}  <- {url[:70]}...")
            r = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
            ct = r.headers.get("Content-Type", "")
            if r.status_code == 200 and (b'%PDF' in r.content[:10] or 'pdf' in ct.lower()):
                dest.write_bytes(r.content)
                size = len(r.content) // 1024
                print(f"       OK  ({size} KB)")
                results[mod].append({"file": fname, "url": url, "status": "ok", "size_kb": size})
            else:
                print(f"       FAIL  status={r.status_code} ct={ct[:40]}")
                results[mod].append({"file": fname, "url": url, "status": f"fail-{r.status_code}"})
        except Exception as e:
            print(f"       ERROR: {e}")
            results[mod].append({"file": fname, "url": url, "status": f"error:{e}"})
        time.sleep(0.5)

print("\n=== SUMMARY ===")
for mod, items in results.items():
    ok = [i for i in items if i['status'] in ('ok','exists')]
    fail = [i for i in items if i['status'] not in ('ok','exists')]
    print(f"Module {mod}: {len(ok)}/{len(items)} OK")
    for i in fail:
        print(f"  FAIL: {i['file']} -> {i['status']}")

with open(BASE / "scripts" / "pdf_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nResults saved to scripts/pdf_results.json")
