"""
Add "Referências Bibliográficas" section after Material de Apoio in each module,
and add a sidebar nav link for it.
"""
import re
from pathlib import Path

BASE = Path(r"c:\Users\AparicioJunior\workspace\saude-caminhoneiros")

# ─── Reference data per module ───────────────────────────────────────────────

REFS = {
    1: [
        "BRASIL. Ministério da Saúde. <em>Política Nacional de Atenção Integral à Saúde da Mulher: princípios e diretrizes</em>. Brasília, DF: Ministério da Saúde, 2004. Disponível em: https://bvsms.saude.gov.br/bvs/publicacoes/politica_nac_atencao_mulher.pdf. Acesso em: 16 mar. 2026.",
        "BRASIL. Ministério da Saúde. Secretaria de Atenção à Saúde. <em>Política Nacional de Atenção Integral à Saúde do Homem: princípios e diretrizes</em>. Brasília, DF: Ministério da Saúde, 2008. Disponível em: https://bvsms.saude.gov.br/bvs/publicacoes/politica_nacional_atencao_saude_homem.pdf. Acesso em: 16 mar. 2026.",
        "BRASIL. Conselho Nacional de Secretários de Saúde (CONASS). <em>Vigilância em Saúde: parte 1</em>. Brasília, DF: CONASS, 2011. (Coleção Para Entender a Gestão do SUS, v. 5). Disponível em: www.conass.org.br/bibliotecav3/pdfs/colecao2011/livro_5.pdf. Acesso em: 16 mar. 2026.",
        "BRASIL. Ministério da Saúde. Portaria nº 2.761, de 19 de novembro de 2013. Institui a Política Nacional de Educação Popular em Saúde no âmbito do Sistema Único de Saúde (PNEPS-SUS). <em>Diário Oficial da União</em>: seção 1, Brasília, DF, 20 nov. 2013a. Disponível em: https://bvsms.saude.gov.br/bvs/saudelegis/gm/2013/prt2761_19_11_2013.html. Acesso em: 4 maio 2026.",
        "BRASIL. Ministério da Saúde. Secretaria de Atenção à Saúde. <em>Acolhimento à demanda espontânea: Queixas mais comuns na Atenção Básica</em>. Brasília, DF: Ministério da Saúde, 2013b. (Cadernos de Atenção Básica, n. 28, v. 2). Disponível em: https://bvsms.saude.gov.br/bvs/publicacoes/acolhimento_demanda_espontanea_queixas_comuns_cab28v2.pdf. Acesso em: 13 abr. 2026.",
        "BRASIL. Ministério da Saúde. <em>Política Nacional de Promoção da Saúde (PNPS): Revisão da Portaria MS/GM nº 687, de 30 de março de 2006</em>. Brasília, DF: Ministério da Saúde, 2014. Disponível em: https://bvsms.saude.gov.br/bvs/publicacoes/pnps_revisao_portaria_687.pdf. Acesso em: 16 mar. 2026.",
        "BRASIL. Ministério da Saúde. Portaria nº 2.436, de 21 de setembro de 2017. Aprova a Política Nacional de Atenção Básica, estabelecendo a revisão de diretrizes para a organização da Atenção Básica no âmbito do Sistema Único de Saúde (SUS). <em>Diário Oficial da União</em>: seção 1, Brasília, DF, 22 set. 2017. Disponível em: https://bvsms.saude.gov.br/bvs/saudelegis/gm/2017/prt2436_22_09_2017.html. Acesso em: 25 maio 2026.",
        "BRASIL. Medida Provisória nº 1.301, de 30 de maio de 2025. Institui o Programa Agora Tem Especialistas. <em>Diário Oficial da União</em>: seção 1, Brasília, DF, 31 maio 2025. Disponível em: www2.camara.leg.br/legin/fed/medpro/2025/medidaprovisoria-1301-30-maio-2025-797527-publicacaooriginal-175524-pe.html. Acesso em: 25 maio 2026.",
        "FREITAS, C. M. et al. Conquistas, limites e obstáculos à redução de riscos ambientais à saúde nos 30 anos do Sistema Único de Saúde. <em>Ciência &amp; Saúde Coletiva</em>, [online], v. 23, n. 6, p. 1981–1996, 2018. Disponível em: www.scielo.br/pdf/csc/v23n6/1413-8123-csc-23-06-1981.pdf. Acesso em: 16 mar. 2026.",
        "GIOVANELLA, L.; FRANCO, C. M.; ALMEIDA, P. F. de. Política Nacional de Atenção Básica: para onde vamos? <em>Ciência &amp; Saúde Coletiva</em>, [online], v. 25, n. 4, p. 1475–1482, 2020. Disponível em: www.scielo.br/j/csc/a/TGQXJ7ZtSNT4BtZJgxYdjYG/?lang=pt. Acesso em: 25 maio 2026.",
        "SILVA, A. C. et al. <em>Saúde e qualidade de vida de caminhoneiros</em>. Curitiba: Editora Científica Digital, 2022. Disponível em: https://downloads.editoracientifica.com.br/articles/220308367.pdf. Acesso em: 18 fev. 2026.",
        "SOUZA, T. S.; VIRGENS, L. S. Saúde do trabalhador na Atenção Básica: interfaces e desafios. <em>Revista Brasileira de Saúde Ocupacional</em>, São Paulo, n. 38, v. 128, p. 292–301, 2013. Disponível em: www.scielo.br/j/rbso/a/ZBBvzDsBkJ3vPFhcJjrq73G/?lang=pt. Acesso em: 25 maio 2026.",
        "STARFIELD, B. <em>Atenção Primária: equilíbrio entre necessidades de saúde, serviços e tecnologia</em>. Brasília, DF: UNESCO; Ministério da Saúde, 2002. Disponível em: www.dominiopublico.gov.br/download/texto/ue000039.pdf. Acesso em: 16 mar. 2026.",
    ],
    2: [
        "AVASUS. <em>Sífilis: diagnóstico e tratamento</em>. Módulo/curso de 30 h oferecido pela Universidade Federal do Rio Grande do Norte/UNA-SUS desde 2023. Disponível em: https://avasus.ufrn.br/local/avasplugin/cursos/curso.php?id=526. Acesso em: 15 abr. 2026.",
        "AVASUS. <em>Infecção pelo HPV</em>. Universidade Federal do Rio Grande do Norte/UNA-SUS, 2020. Disponível em: https://avasus.ufrn.br/local/avasplugin/cursos/curso.php?id=386. Acesso em: 21 maio 2026.",
        "BRASIL. Ministério da Saúde. Secretaria de Atenção Primária à Saúde. Nota Técnica nº 8/2020. Trata da apresentação e implementação do Cartão de Saúde do Caminhoneiro e da Caminhoneira. Brasília: Ministério da Saúde, 2020. Disponível em: https://egestorab.saude.gov.br/image/?file=20210430_N_SEI25000.156178202097_1396110966499381938.pdf. Acesso em: 21 maio 2026.",
        "BRASIL. Ministério da Saúde. Secretaria de Vigilância em Saúde. <em>Protocolo clínico e diretrizes terapêuticas para atenção integral às pessoas com infecções sexualmente transmissíveis (IST)</em>. Brasília: Ministério da Saúde, 2022. Disponível em: www.gov.br/aids/pt-br/central-de-conteudo/pcdts/2022/ist/pcdt-ist-2022_isbn-1.pdf/@@display-file/file. Acesso em: 21 maio 2026.",
        "BRASIL. Ministério da Saúde. <em>Ministério da Saúde volta a distribuir gel lubrificante</em>. [online]: Ministério da Saúde, 7 nov. 2023a. Disponível em: www.gov.br/aids/pt-br/assuntos/noticias/2023/outubro/ministerio-da-saude-volta-a-distribuir-gel-lubrificante. Acesso em: 5 mar. 2026.",
        "BRASIL. Ministério da Saúde. Secretaria de Vigilância em Saúde e Ambiente. <em>Manual dos Centros de Referência para Imunobiológicos Especiais</em>. 6. ed. Brasília: Ministério da Saúde, 2023b. Disponível em: http://bvsms.saude.gov.br/bvs/publicacoes/manual_centros_referencia_imunobiologicos_6ed.pdf. Acesso em: 5 mar. 2026.",
        "BRASIL. Ministério da Saúde. <em>HPV: informações sobre a infecção</em>. [online]: Ministério da Saúde, 15 jul. 2024a. Disponível em: www.gov.br/aids/pt-br/assuntos/ist/hpv. Acesso em: 5 mar. 2026.",
        "BRASIL. Ministério da Saúde. <em>Pacientes com papilomatose respiratória recorrente são incluídos no grupo prioritário para vacina do HPV</em>. [online]: Ministério da Saúde, 27 abr. 2024b. Disponível em: www.gov.br/saude/pt-br/assuntos/noticias/2024/abril/pacientes-com-papilomatose-respiratoria-recorrente-sao-incluidos-no-grupo-prioritario-para-vacina-do-hpv. Acesso em: 10 maio 2026.",
        "BRASIL. Ministério da Saúde. <em>Protocolo Clínico e Diretrizes Terapêuticas para Manejo da Infecção pelo HIV em Adultos</em>. Brasília: Ministério da Saúde, 2024c. Disponível em: www.gov.br/aids/pt-br/central-de-conteudo/pcdts/pcdt_hiv_modulo_1_2024.pdf. Acesso em: 21 maio 2026.",
        "BRASIL. Ministério da Saúde. Secretaria de Ciência, Tecnologia, Inovação e Complexo da Saúde; Secretaria de Vigilância em Saúde e Ambiente. <em>Protocolo Clínico e Diretrizes Terapêuticas para Profilaxia Pós-Exposição de Risco (PEP) à Infecção por HIV, ISTs e Hepatites Virais</em>. Brasília: Ministério da Saúde, 2024d. Disponível em: www.gov.br/aids/pt-br/central-de-conteudo/pcdts/2021/hiv-aids/prot_clinico_diretrizes_terap_pep_-risco_infeccao_hiv_ist_hv_2021.pdf/@@display-file/file. Acesso em: 21 maio 2026.",
        "BRASIL. Ministério da Saúde. Secretaria de Vigilância em Saúde e Ambiente. <em>Guia de vigilância em saúde</em>. vol. 2. 6. ed. rev. Brasília: Ministério da Saúde, 2024e. Disponível em: https://bvsms.saude.gov.br/bvs/publicacoes/guia_vigilancia_saude_v2_6edrev.pdf. Acesso em: 13 mar. 2026.",
        "BRASIL. Ministério da Saúde. Secretaria de Ciência, Tecnologia, Inovação e Complexo da Saúde; Secretaria de Vigilância em Saúde e Ambiente. <em>Protocolo Clínico e Diretrizes Terapêuticas para Profilaxia Pré-Exposição (PrEP) Oral à Infecção pelo HIV</em>. Brasília: Ministério da Saúde, 2025a. Disponível em: www.gov.br/aids/pt-br/central-de-conteudo/pcdts/protocolo-clinico-e-diretrizes-terapeuticas-para-profilaxia-pre-exposicao-prep-oral-a-infeccao-pelo-hiv.pdf/@@display-file/file. Acesso em: 21 maio 2026.",
        "BRASIL. Ministério da Saúde. <em>Ministério da Saúde amplia vacinação contra hepatite A para usuários de PrEP</em>. [online]: Ministério da Saúde, 2 maio 2025b. Disponível em: www.gov.br/saude/pt-br/assuntos/noticias/2025/maio/ministerio-da-saude-amplia-vacinacao-contra-hepatite-a-para-usuarios-de-prep. Acesso em: 5 mar. 2026.",
        "BRASIL. Ministério da Saúde. <em>Campanha de Carnaval do Ministério da Saúde reforça uso de camisinha na prevenção de doenças</em>. [online]: Ministério da Saúde, 13 fev. 2026a. Disponível em: www.gov.br/saude/pt-br/assuntos/noticias/2026/fevereiro/campanha-de-carnaval-do-ministerio-da-saude-reforca-uso-de-camisinha-na-prevencao-de-doencas-adesao-ao-preservativo-esta-em-queda. Acesso em: 5 mar. 2026.",
        "BRASIL. Ministério da Saúde. <em>Instrução Normativa do Calendário Nacional de Vacinação 2026</em>. Brasília: Ministério da Saúde, 2026b. Disponível em: www.gov.br/saude/pt-br/vacinacao/publicacoes/instrucao-normativa-que-instrui-o-calendario-nacional-de-vacinacao-2026.pdf. Acesso em: 5 mar. 2026.",
        "CENTERS FOR DISEASE CONTROL AND PREVENTION. <em>Preventing HIV with Condoms</em>. [online]: CDC, 24 abr. 2024. Disponível em: www.cdc.gov/hiv/prevention/condoms.html. Acesso em: 5 mar. 2026.",
        "HANDSFIELD, H. H.; SPARLING, P. F. Neisseria Gonnorrhoea. In: MANDELL, G. L.; BENNETT, J. E.; DOLIN, R. <em>Mandell, Douglas, and Bennett's principles and practice of infectious diseases</em>. 4. ed. Nova York: Churchill Livingstone, 1995. p. 1909–1927.",
        "LO RE, V. 3RD. et al. State-of-the-Art Review: Hepatitis C. <em>Clinical Infectious Diseases</em>, v. 81, n. 2, p. e15–e26, 2025. Disponível em: https://pubmed.ncbi.nlm.nih.gov/40971900/. Acesso em: 14 mar. 2026.",
        "MAGALHÃES, G. M. et al. Update on human papillomavirus - part I: epidemiology, pathogenesis, and clinical spectrum. <em>Anais Brasileiros de Dermatologia</em>, Rio de Janeiro, v. 96, n. 1, p. 1–16, 2021. Disponível em: https://pubmed.ncbi.nlm.nih.gov/33341319/. Acesso em: 21 maio 2026.",
        "MCCREE, D. H. et al. Sexual and drugs use risk behaviors of long-haul truck drivers and their commercial sex contacts in New Mexico. <em>Public Health Reports</em>, Thousand Oaks, v. 125, n. 1, p. 52–60, 2010. Disponível em: https://journals.sagepub.com/doi/10.1177/003335491012500108. Acesso em: 21 maio 2026.",
        "OLIVEIRA, F. D. B.; ARAÚJO, M. A. L. Sexual behavior and preventive practices among truck drivers to prevent sexually transmitted infections. <em>Revista Gaúcha de Enfermagem</em>, v. 46, n. spe1, 2025. Disponível em: www.scielo.br/j/rgenf/a/VhZDqQry6YCxKDP7t9qc7bf/?lang=en. Acesso em: 5 mar. 2026.",
        "RIBEIRO, M. Secretaria Estadual da Saúde (RS). <em>Comando de saúde preventivo realiza ação com caminhoneiros em Osório</em>. [online]: Secretaria da Saúde (RS), 10 mar. 2025. Disponível em: https://saude.rs.gov.br/comando-de-saude-preventivo-realiza-acao-com-caminhoneiros-em-osorio. Acesso em: 1 abr. 2026.",
        "ROWLEY, J. et al. Chlamydia, gonorrhea, trichomoniasis and syphilis: global prevalence and incidence estimates, 2016. <em>Bulletin of the World Health Organization</em>, Genebra, v. 97, n. 8, p. 548–562, 2019. Disponível em: https://pmc.ncbi.nlm.nih.gov/articles/PMC6653813/pdf/BLT.18.228486.pdf. Acesso em: 14 mar. 2026.",
        "SANTOS, M. C. Q. et al. Marcadores de vulnerabilidade em saúde sexual: uma análise comparativa entre caminhoneiros e a população brasileira. <em>Cadernos Cajuína</em>, v. 11, n. 4, 2026. Disponível em: https://v3.cadernoscajuina.pro.br/index.php/revista/article/view/2534. Acesso em: 14 abr. 2026.",
        "SAUERBREI, A. Herpes Genitalis: Diagnosis, Treatment and Prevention. <em>Geburtshilfe Frauenheilkd</em>, Stuttgart, v. 76, n. 12, p. 1310–1317, 2016. Disponível em: https://pubmed.ncbi.nlm.nih.gov/28017972/. Acesso em: 14 mar. 2026.",
        "STELA, D. Prefeitura Municipal de Sinop. Secretaria Municipal de Saúde. <em>Saúde faz distribuição de preservativos em pontos estratégicos com foco na prevenção de IST</em>. [online]: Prefeitura de Sinop, 28 jun. 2023. Disponível em: www.sinop.mt.gov.br/portal/noticias/0/3/920/saude-faz-distribuicao-de-preservativos-em-pontos-estrategicos-com-foco-na-prevencao-de-ists. Acesso em: 5 mar. 2026.",
        "VILLARINHO, L. et al. Caminhoneiros de rota curta e sua vulnerabilidade ao HIV, Santos, SP. <em>Revista de Saúde Pública</em>, São Paulo, v. 36, n. 4, p. 61–67, 2002. Disponível em: www.scielo.br/j/rsp/a/phXRzW38VG6d5khG8sJtTJv/abstract/?lang=pt. Acesso em: 5 mar. 2026.",
        "WHO (WORLD HEALTH ORGANIZATION). <em>Use and procurement of additional lubricants for male and female condoms: advisory note</em>. Geneva: WHO/UNFPA/FHI360, 2012. Disponível em: https://iris.who.int/handle/10665/76580. Acesso em: 5 mar. 2026.",
        "WHO (WORLD HEALTH ORGANIZATION). <em>Consolidated guidelines on HIV prevention, diagnosis, treatment and care for key populations: 2016 update</em>. Genebra: WHO, 2016. Disponível em: https://iris.who.int/server/api/core/bitstreams/918a4a9a-5116-49d7-9074-e7bcf295d0b6/content. Acesso em: 21 maio 2026.",
        "WHO (WORLD HEALTH ORGANIZATION). <em>Sexually Transmitted Infections (STIs)</em>. [online]: World Health Organization, 10 set. 2025. Disponível em: www.who.int/news-room/fact-sheets/detail/sexually-transmitted-infections-(stis). Acesso em: 14 mar. 2026.",
    ],
    3: [
        "APA (ASSOCIAÇÃO AMERICANA DE PSIQUIATRIA). <em>Manual diagnóstico e estatístico de transtornos mentais</em>. Tradução de Maria Inês Corrêa Nascimento et al. 5. ed. Porto Alegre: Artmed, 2014. Disponível em: https://membros.analysispsicologia.com.br/wp-content/uploads/2024/06/DSM-V.pdf. Acesso em: 27 maio 2026.",
        "BRASIL. Lei nº 13.103, de 2 de março de 2015. Dispõe sobre o exercício da profissão de motorista; altera a Consolidação das Leis do Trabalho (CLT) e outras legislações. <em>Diário Oficial da União</em>: seção 1, Brasília, DF, p. 1, 3 mar. 2015. Disponível em: www2.camara.leg.br/legin/fed/lei/2015/lei-13103-2-marco-2015-780193-norma-pl.html. Acesso em: 27 maio 2026.",
        "BRASIL. Ministério da Saúde. Portaria nº 3.088, de 23 de dezembro de 2011. Institui a Rede de Atenção Psicossocial para pessoas com sofrimento ou transtorno mental e com necessidades decorrentes do uso de crack, álcool e outras drogas, no âmbito do SUS. <em>Diário Oficial da União</em>: seção 1, Brasília, DF, p. 59, 26 dez. 2011. Disponível em: https://bvsms.saude.gov.br/bvs/saudelegis/gm/2011/prt3088_23_12_2011_rep.html. Acesso em: 27 maio 2026.",
        "CERQUEIRA, E. S.; SANTANA, M. V. M. Satisfação no trabalho entre profissionais do transporte rodoviário: estudo comparativo entre autônomos e empregados. <em>Revista de Psicologia</em>, v. 5, n. 1, p. 109–120, 2014. Disponível em: https://dialnet.unirioja.es/servlet/articulo?codigo=8086132. Acesso em: 19 fev. 2026.",
        "CHILDHOOD BRASIL. <em>O Perfil do Caminhoneiro Brasileiro</em>. 5. ed. São Paulo: Childhood Brasil; Programa Na Mão Certa, 2025. Disponível em: https://namaocerta.org.br/pesquisas-e-publicacoes/o-perfil-do-caminhoneiro-brasileiro-2025/. Acesso em: 27 maio 2026.",
        "KNAUTH, D. R. et al. Manter-se acordado: a vulnerabilidade dos caminhoneiros no Rio Grande do Sul. <em>Revista de Saúde Pública</em>, v. 46, n. 5, p. 886–893, 2012. Disponível em: www.scielo.br/j/rsp/a/qqzWhf4Mp6TTysBf6pZCXfz/?lang=pt. Acesso em: 19 fev. 2026.",
        "LEOPOLDO, K.; LEYTON, V.; OLIVEIRA, L. G. Uso exclusivo de álcool e em associação a outras drogas entre motoristas de caminhão que trafegam por rodovias do Estado de São Paulo, Brasil: um estudo transversal. <em>Cadernos de Saúde Pública</em>, v. 31, n. 9, 2015. Disponível em: www.scielo.br/j/csp/a/vvmfh6xvtDT9xGx4xkmh4Qq/abstract/?lang=pt. Acesso em: 27 maio 2026.",
        "MASSON, V. A.; MONTEIRO, M. I. Estilo de vida, aspectos de saúde e trabalho de motoristas de caminhão. <em>Revista Brasileira de Enfermagem</em>, v. 63, n. 4, p. 533–540, 2010. Disponível em: www.scielo.br/j/reben/a/SfX3fnBfK7bfVtFbFzMHtPD/?lang=pt. Acesso em: 19 fev. 2026.",
        "NASCIMENTO, E. C.; NASCIMENTO, E.; SILVA, J. P. Uso de álcool e anfetaminas entre caminhoneiros de estrada. <em>Revista de Saúde Pública</em>, São Paulo, v. 41, n. 2, p. 290–293, 2007. Disponível em: www.scielo.br/j/rsp/a/b9vVFYzYSf6fCH9djV9s6nH/?lang=pt. Acesso em: 27 maio 2026.",
        "POLÍCIA RODOVIÁRIA FEDERAL (PRF). <em>Anuário Estatístico de Acidentes de Trânsito nas Rodovias Federais</em>. Brasília: PRF, 2023. Disponível em: www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/diest-arquivos/anuario-2023_final.html. Acesso em: 27 maio 2026.",
        "VIANA, S.; FEITOSA, J.; CERQUEIRA-SANTOS, E. Saúde mental de caminhoneiros: preditores demográficos e condições de trabalho. <em>Revista Saúde e Desenvolvimento Humano</em>, Canoas, v. 13, n. 2, 2025. Disponível em: https://revistas.unilasalle.edu.br/index.php/saude_desenvolvimento/article/view/12894. Acesso em: 19 fev. 2026.",
    ],
    4: [
        "BRASIL. Ministério da Saúde. Portaria nº 2.336, de 21 de setembro de 2017. Aprova a Política Nacional de Atenção Básica, estabelecendo a revisão de diretrizes para a organização da Atenção Básica, no âmbito do Sistema Único de Saúde (SUS). <em>Diário Oficial da União</em>: seção 1, Brasília, DF, 22 set. 2017. Disponível em: https://bvsms.saude.gov.br/bvs/saudelegis/gm/2017/prt2436_22_09_2017.html. Acesso em: 20 fev. 2026.",
        "BRASIL. Ministério da Saúde. Secretaria de Atenção à Saúde. <em>Estratégias para o cuidado da pessoa com doença crônica</em>. Brasília, DF: Ministério da Saúde, 2014. (Cadernos de Atenção Básica, n. 35). Disponível em: https://bvsms.saude.gov.br/bvs/publicacoes/estrategias_cuidado_pessoa_doenca_cronica_cab35.pdf. Acesso em: 20 fev. 2026.",
        "BRASIL. Ministério da Saúde. Secretaria de Vigilância em Saúde. <em>Plano de Ações Estratégicas para o Enfrentamento das Doenças Crônicas e Agravos não Transmissíveis no Brasil 2021–2030</em>. Brasília, DF: Ministério da Saúde, 2021a. Disponível em: www.gov.br/saude/pt-br/centrais-de-conteudo/publicacoes/svsa/doencas-cronicas-nao-transmissiveis-dcnt/09-plano-de-dant-2022_2030.pdf. Acesso em: 20 fev. 2026.",
        "BRASIL. Ministério da Saúde. Secretaria de Atenção Primária à Saúde. <em>Manual de atenção às pessoas com sobrepeso e obesidade no âmbito da Atenção Primária à Saúde do Sistema Único de Saúde</em>. Brasília, DF: Ministério da Saúde, 2021b. Disponível em: https://bvsms.saude.gov.br/bvs/publicacoes/manual_atencao_pessoas_sobrepeso_obesidade.pdf. Acesso em: 1 mar. 2026.",
        "BRASIL. Ministério da Saúde. <em>Protocolo Clínico e Diretrizes Terapêuticas Diabete Melito Tipo 2</em>. Brasília, DF: Ministério da Saúde, 2022. Disponível em: www.gov.br/saude/pt-br/assuntos/pcdt/d/diabete-melito-tipo-2.pdf/view. Acesso em: 20 fev. 2026.",
        "BRASIL. Instituto Nacional de Câncer (INCA). <em>Câncer de pele não melanoma</em>. Rio de Janeiro: INCA, atualizado em 27 maio 2025. Disponível em: www.gov.br/inca/pt-br/assuntos/cancer/tipos/pele-nao-melanoma. Acesso em: 15 maio 2026.",
        "CHILDHOOD BRASIL. <em>O Perfil do Caminhoneiro Brasileiro</em>. 5. ed. São Paulo: Childhood Brasil; Programa Na Mão Certa, 2025. Disponível em: https://namaocerta.org.br/pesquisas-e-publicacoes/o-perfil-do-caminhoneiro-brasileiro-2025/. Acesso em: 20 fev. 2026.",
        "KRISHNAMOORTHY, Y.; SARVESWARAN, G.; SAKTHIVEL, M. Prevalence of hypertension among professional drivers: Evidence from 2000 to 2017: A systematic review and meta-analysis. <em>Journal of Postgraduated Medicine</em>, v. 66, n. 2, p. 81–89, 2020. Disponível em: https://journals.lww.com/jopm/fulltext/2020/66020/prevalence_of_hypertension_among_professional.6.aspx. Acesso em: 20 maio 2026.",
        "REIS, L. A. P. et al. Obesity, hypertension and diabetes among truck drivers in the middle-west, Brazil. <em>Bioscience Journal</em>, Uberlândia, v. 33, n. 2, p. 485–493, 2017. Disponível em: www.researchgate.net/publication/315920374_Obesity_hypertension_and_diabetes_among_truck_drivers_in_the_middle-west_Brazil. Acesso em: 20 maio 2026.",
        "SBD (SOCIEDADE BRASILEIRA DE DIABETES). <em>Diretriz da Sociedade Brasileira de Diabetes – Edição 2025</em>. [S. l.], 2025. Disponível em: https://diretriz.diabetes.org.br/. Acesso em: 20 maio 2026.",
        "ZAMPARONI VICTORINO, S. V. et al. A look through Latin America truck drivers' health, a systematic review and meta-analysis. <em>BMC Public Health</em>, v. 23, 2023. Disponível em: https://link.springer.com/article/10.1186/s12889-022-14902-2. Acesso em: 20 maio 2026.",
    ],
    5: [
        "BRASIL. Presidência da República. Lei nº 11.340, de 7 de agosto de 2006. Cria mecanismos para coibir a violência doméstica e familiar contra a mulher. <em>Diário Oficial da União</em>: seção 1, Brasília, DF, 8 ago. 2006a. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2006/lei/l11340.htm. Acesso em: 21 maio 2026.",
        "BRASIL. Ministério da Saúde. <em>Prevenção do suicídio: manual dirigido a profissionais das equipes de saúde mental</em>. Brasília, DF: Ministério da Saúde, 2006b. Disponível em: https://cvv.org.br/wp-content/uploads/2023/08/manual_prevencao_suicidio_profissionais_saude.pdf. Acesso em: 21 maio 2026.",
        "BRASIL. Ministério da Saúde. <em>Linha de cuidado para a atenção integral à saúde de crianças, adolescentes e suas famílias em situação de violência: orientação para gestores e profissionais de saúde</em>. Brasília, DF: Ministério da Saúde, 2011. Disponível em: www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/s/saude-da-crianca/publicacoes/linha-de-cuidado-para-a-atencao-integral-a-saude-de-criancas-adolescentes-e-suas-familias-em-situacao-de-violencias-orientacao-para-gestores-e-profissionais-de-saude/view. Acesso em: 21 maio 2026.",
        "BRASIL. Ministério da Saúde. Portaria de Consolidação nº 2, de 28 de setembro de 2017. Consolidação das normas sobre as políticas nacionais de saúde do Sistema Único de Saúde. Anexo VII: Política Nacional de Redução da Morbimortalidade por Acidentes e Violências. <em>Diário Oficial da União</em>: seção 1, Brasília, DF, 3 out. 2017. Disponível em: https://bvsms.saude.gov.br/bvs/saudelegis/gm/2017/prc0002_03_10_2017.html#ANEXOVII. Acesso em: 21 maio 2026.",
        "BRASIL. Ministério da Saúde. Secretaria de Atenção Primária à Saúde. <em>O cuidado à saúde do homem em contexto de violência e a proteção de meninas e mulheres no âmbito da APS: caderno didático do curso</em>. Brasília, DF: Ministério da Saúde, 2025. Disponível em: http://bvsms.saude.gov.br/bvs/publicacoes/cuidado_saude_homem_contexto_violencia.pdf. Acesso em: 21 maio 2026.",
        "CONNELL, R. <em>Masculinities</em>. 2. ed. Berkeley: University of California Press, 2005.",
        "CONNELL, R. <em>Gênero em termos reais</em>. São Paulo: nVersos Editora, 2016.",
        "CONNELL, R.; PEARSE, R. <em>Gênero: uma perspectiva global</em>. São Paulo: nVersos Editora, 2015.",
        "COSTA, R. G. Saúde e masculinidade: reflexões de uma perspectiva de gênero. <em>Revista Brasileira de Estudos de População</em>, São Paulo, v. 20, n. 1, p. 79–92, 2003. Disponível em: https://rebep.org.br/revista/article/view/305. Acesso em: 21 maio 2026.",
        "MISSE, M. Violência e teoria social. <em>Dilemas: Revista de Estudos de Conflito e Controle Social</em>, Rio de Janeiro, v. 9, n. 1, p. 45–63, 2016. Disponível em: https://revistas.ufrj.br/index.php/dilemas/article/view/7672. Acesso em: 21 maio 2026.",
        "SCOTT, J. Gênero: uma categoria útil de análise histórica. <em>Revista Educação &amp; Realidade</em>, Porto Alegre, v. 20, n. 2, p. 71–99, 1995. Disponível em: https://archive.org/stream/scott_gender#page/n8/mode/1up. Acesso em: 21 maio 2026.",
        "TAVARES DOS SANTOS, J. V. <em>Violências e conflitualidades</em>. Porto Alegre: Tomo editorial, 2009.",
        "TONELI, M. J. F.; SOUZA, M. G. C.; MÜLLER, R. Masculinidades e práticas de saúde: retratos da experiência de pesquisa em Florianópolis/SC. <em>Physis: Revista de Saúde Coletiva</em>, Rio de Janeiro, v. 20, n. 3, p. 973–994, 2010. Disponível em: www.scielo.br/j/physis/a/VZK8T9ZQw5Cr6W7ZpW8wzFp/?lang=pt. Acesso em: 21 maio 2026.",
        "VASCONCELOS, M. F. F.; SEFFNER, F.; MELO, M. R. \"Gente é mais que homem\": gênero e cuidados em álcool e outras drogas. <em>Educar em Revista</em>, v. 36, e75406, 2020. Disponível em: https://pdfs.semanticscholar.org/1e17/6ee6cc7d10bb993553e11ec9bfcc3c27a474.pdf. Acesso em: 21 maio 2026.",
    ],
}

# Module-specific CSS variable prefix
MOD_VARS = {1: "m1", 2: "m2", 3: "m3", 4: "m4", 5: "m5"}

# ─── Build section HTML ───────────────────────────────────────────────────────

def build_section(mod_num, indent="      "):
    mv = MOD_VARS[mod_num]
    items = "\n".join(
        f'{indent}  <li style="padding-left:.25rem">{ref}</li>'
        for ref in REFS[mod_num]
    )
    return (
        f'\n{indent}<!-- ═══ REFERÊNCIAS BIBLIOGRÁFICAS ═══ -->\n'
        f'{indent}<section id="referencias" class="block" style="scroll-margin-top:80px;margin-bottom:2rem">\n'
        f'{indent}  <h2 class="block-title" style="color:var(--{mv}-primary-deep);margin-bottom:1.5rem">Referências Bibliográficas</h2>\n'
        f'{indent}  <ol style="padding-left:1.5rem;display:flex;flex-direction:column;gap:.85rem;'
        f'color:var(--fg2);font-size:.88rem;line-height:1.65;">\n'
        f'{items}\n'
        f'{indent}  </ol>\n'
        f'{indent}</section>\n'
    )

# ─── Apply to each module ─────────────────────────────────────────────────────

for mod_num in range(1, 6):
    path = BASE / f"modulo {mod_num}" / "index.html"
    content = path.read_text(encoding="utf-8")

    if 'id="referencias"' in content:
        print(f"M{mod_num}: already has referencias section, skipping")
        continue

    # 1. Insert section — find last </section> immediately before </main>
    #    Pattern: </section>\n\n    </main>  (with varying indent)
    pattern = r'(</section>\n)\n(\s*</main>)'
    # Use rfind approach: split on last occurrence
    # Find all matches and use the last one
    matches = list(re.finditer(pattern, content))
    if not matches:
        # Try without blank line
        pattern = r'(</section>\n)(\s*</main>)'
        matches = list(re.finditer(pattern, content))

    if not matches:
        print(f"M{mod_num}: ERROR — could not find </section>...</main> pattern")
        continue

    m = matches[-1]  # last occurrence = after Material de Apoio
    # Determine indentation from what's before </section>
    before = content[:m.start()]
    last_newline = before.rfind('\n')
    indent = ""
    if last_newline >= 0:
        line_start = before[last_newline+1:]
        indent = " " * (len(line_start) - len(line_start.lstrip()))
    if not indent:
        indent = "      "

    section_html = build_section(mod_num, indent)
    # Insert after the closing </section>, before </main>
    insert_pos = m.start() + len(m.group(1))
    content = content[:insert_pos] + section_html + content[insert_pos:]

    # 2. Add sidebar link after href="#encerramento"
    old_link = '<a class="sidebar-nav__link" href="#encerramento">Encerramento</a>'
    new_link = (
        '<a class="sidebar-nav__link" href="#encerramento">Encerramento</a>\n'
        '        <a class="sidebar-nav__link" href="#referencias">Referências</a>'
    )
    if old_link in content:
        content = content.replace(old_link, new_link, 1)
    else:
        print(f"M{mod_num}: WARNING — sidebar encerramento link not found")

    path.write_text(content, encoding="utf-8")
    ref_count = len(REFS[mod_num])
    print(f"M{mod_num}: OK — {ref_count} referencias added, sidebar updated")

print("\nVerifying...")
for mod_num in range(1, 6):
    path = BASE / f"modulo {mod_num}" / "index.html"
    c = path.read_text(encoding="utf-8")
    has_sec = 'id="referencias"' in c
    has_link = 'href="#referencias"' in c
    print(f"M{mod_num}: section={has_sec}, sidebar_link={has_link}")
