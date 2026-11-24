import random
import tkinter as tk
import unicodedata
from pathlib import Path

import customtkinter as ctk

# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Dicionários divididos por Dificuldade e Continente
paises_por_fase = {
    "Fase 1: Américas (Fácil)": {
        "br": "brasil",
        "ar": "argentina",
        "us": "estados unidos",
        "ca": "canadá",
        "mx": "méxico",
        "cl": "chile",
        "co": "colômbia",
        "uy": "uruguai",
        "py": "paraguai",
        "pe": "peru",
        "cr": "costa rica",
        "cu": "cuba",
        "jm": "jamaica",
        "bo": "bolívia",
    },
    "Fase 2: Europa (Médio)": {
        "fr": "frança",
        "de": "alemanha",
        "it": "itália",
        "es": "espanha",
        "pt": "portugal",
        "gb": "reino unido",
        "nl": "holanda",
        "be": "bélgica",
        "ch": "suíça",
        "se": "suécia",
        "no": "noruega",
        "dk": "dinamarca",
        "gr": "grécia",
        "ru": "rússia",
        "pl": "polônia",
        "at": "áustria",
        "ie": "irlanda",
        "hu": "hungria",
    },
    "Fase 3: Ásia & Oceania (Difícil)": {
        "jp": "japão",
        "cn": "china",
        "kr": "coréia do sul",
        "in": "índia",
        "au": "austrália",
        "nz": "nova zelândia",
        "th": "tailândia",
        "vn": "vietnã",
        "id": "indonésia",
        "ph": "filipinas",
        "sg": "singapura",
        "pk": "paquistão",
        "sa": "arábia saudita",
        "qa": "catar",
        "ae": "emirados árabes unidos",
        "il": "israel",
    },
    "Fase 4: África (Desafio Final)": {
        "za": "áfrica do sul",
        "eg": "egito",
        "ng": "nigéria",
        "ma": "marrocos",
        "gh": "ganas",
        "ke": "quênia",
        "sn": "senegal",
        "ao": "angola",
        "mz": "moçambique",
        "dz": "argélia",
        "tn": "tunísia",
        "cm": "camarões",
        "cv": "cabo verde",
        "et": "etiópia",
    },
}

TOTAL_PERGUNTAS = 10


def remover_acentos(texto):
  nfkd = unicodedata.normalize("NFD", texto)
  return "".join([c for c in nfkd if not unicodedata.combining(c)])


class JogoBandeirasApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Jogo das Bandeiras - Modo Continentes")
    self.root.geometry("520x660")
    self.root.resizable(False, False)

    self.COR_FUNDO_PADRAO = "#2b2b2b"
    self.COR_CARD = "#333333"

    self.j1 = ""
    self.j2 = ""
    self.pontos_j1 = 0
    self.pontos_j2 = 0

    self.jogador_atual = 1
    self.rodada_atual = 1
    self.perguntas_j1 = []
    self.perguntas_j2 = []
    self.pergunta_atual = None

    self.animacao_fogos_ativa = False
    self.imagens_bandeiras = {}

    pasta_bandeiras = Path(__file__).resolve().parent / "assets" / "flags"
    codigos_bandeiras = dict.fromkeys(
        codigo
        for fase in paises_por_fase.values()
        for codigo in fase
    )
    for codigo in codigos_bandeiras:
      caminho = pasta_bandeiras / f"{codigo}.png"
      if not caminho.is_file():
        raise FileNotFoundError(f"Imagem de bandeira não encontrada: {caminho}")
      self.imagens_bandeiras[codigo] = tk.PhotoImage(
          master=self.root, file=str(caminho)
      )

    self.criar_tela_inicio()

  def limpar_tela(self):
    self.animacao_fogos_ativa = False
    self.root.configure(fg_color=self.COR_FUNDO_PADRAO)
    for widget in self.root.winfo_children():
      widget.destroy()

  # --- TELA 1: CADASTRO DOS JOGADORES ---
  def criar_tela_inicio(self):
    self.limpar_tela()

    titulo = ctk.CTkLabel(
        self.root,
        text="JOGO DAS BANDEIRAS",
        font=ctk.CTkFont(size=24, weight="bold"),
        text_color="#f1c40f",
    )
    titulo.pack(pady=(25, 2))

    subtitulo = ctk.CTkLabel(
        self.root,
        text="Modo Campanha: Turnos Alternados por Continente",
        font=ctk.CTkFont(size=13, weight="normal"),
        text_color="#2ecc71",
    )
    subtitulo.pack(pady=(0, 20))

    card = ctk.CTkFrame(self.root, corner_radius=15, fg_color=self.COR_CARD)
    card.pack(pady=10, padx=40, fill="both", expand=True)

    ctk.CTkLabel(
        card,
        text="Nome do Jogador 1:",
        font=ctk.CTkFont(size=14, weight="bold"),
    ).pack(pady=(20, 5))
    self.ent_j1 = ctk.CTkEntry(
        card,
        placeholder_text="Ex: Alex",
        width=250,
        height=35,
        corner_radius=10,
    )
    self.ent_j1.pack(pady=5)

    ctk.CTkLabel(
        card,
        text="Nome do Jogador 2:",
        font=ctk.CTkFont(size=14, weight="bold"),
    ).pack(pady=(15, 5))
    self.ent_j2 = ctk.CTkEntry(
        card,
        placeholder_text="Ex: Maria",
        width=250,
        height=35,
        corner_radius=10,
    )
    self.ent_j2.pack(pady=5)

    btn_iniciar = ctk.CTkButton(
        card,
        text="Iniciar Desafio",
        font=ctk.CTkFont(size=15, weight="bold"),
        fg_color="#27ae60",
        hover_color="#219653",
        text_color="white",
        height=40,
        corner_radius=20,
        command=self.iniciar_jogo,
    )
    btn_iniciar.pack(pady=25)

    btn_historico = ctk.CTkButton(
        self.root,
        text="Ver Histórico",
        font=ctk.CTkFont(size=13),
        fg_color="#2980b9",
        hover_color="#1f618d",
        text_color="white",
        corner_radius=15,
        command=self.mostrar_historico,
    )
    btn_historico.pack(pady=20)

  def sortear_perguntas_sem_repeticao(self):
    """Sorteia 20 perguntas no total (sem repetição entre J1 e J2) divididas igualmente em 10 para cada jogador."""
    # Sorteia o dobro de perguntas de cada fase sem repetir países
    f1 = random.sample(
        list(paises_por_fase["Fase 1: Américas (Fácil)"].items()), 6
    )
    f2 = random.sample(
        list(paises_por_fase["Fase 2: Europa (Médio)"].items()), 6
    )
    f3 = random.sample(
        list(paises_por_fase["Fase 3: Ásia & Oceania (Difícil)"].items()), 6
    )
    f4 = random.sample(
        list(paises_por_fase["Fase 4: África (Desafio Final)"].items()), 2
    )

    # Distribui 3 das Américas, 3 da Europa, 3 da Ásia/Oceania e 1 da África para o J1
    j1_perguntas = (
        [(item, "Fase 1: Américas (Fácil)") for item in f1[:3]]
        + [(item, "Fase 2: Europa (Médio)") for item in f2[:3]]
        + [(item, "Fase 3: Ásia & Oceania (Difícil)") for item in f3[:3]]
        + [(item, "Fase 4: África (Desafio Final)") for item in f4[:1]]
    )

    # Distribui os outros países não repetidos para o J2
    j2_perguntas = (
        [(item, "Fase 1: Américas (Fácil)") for item in f1[3:]]
        + [(item, "Fase 2: Europa (Médio)") for item in f2[3:]]
        + [(item, "Fase 3: Ásia & Oceania (Difícil)") for item in f3[3:]]
        + [(item, "Fase 4: África (Desafio Final)") for item in f4[1:]]
    )

    j1_perguntas.reverse()
    j2_perguntas.reverse()

    return j1_perguntas, j2_perguntas

  def iniciar_jogo(self):
    self.j1 = self.ent_j1.get().strip() or "Jogador 1"
    self.j2 = self.ent_j2.get().strip() or "Jogador 2"
    self.pontos_j1 = 0
    self.pontos_j2 = 0

    self.rodada_atual = 1
    self.jogador_atual = 1

    # Gera perguntas exclusivas para ambos os jogadores
    self.perguntas_j1, self.perguntas_j2 = (
        self.sortear_perguntas_sem_repeticao()
    )

    self.criar_tela_pergunta()
    self.proxima_pergunta()

  # --- TELA 2: PERGUNTAS DO JOGO ---
  def criar_tela_pergunta(self):
    self.limpar_tela()

    self.lbl_turno = ctk.CTkLabel(
        self.root,
        text="",
        font=ctk.CTkFont(size=20, weight="bold"),
        text_color="#f1c40f",
    )
    self.lbl_turno.pack(pady=(10, 2))

    self.lbl_placar_parcial = ctk.CTkLabel(
        self.root,
        text="",
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color="#2ecc71",
    )
    self.lbl_placar_parcial.pack(pady=(0, 2))

    self.lbl_fase = ctk.CTkLabel(
        self.root,
        text="",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color="#3498db",
    )
    self.lbl_fase.pack(pady=(0, 2))

    self.lbl_status = ctk.CTkLabel(
        self.root,
        text=f"Rodada 1 de {TOTAL_PERGUNTAS}",
        font=ctk.CTkFont(size=12),
        text_color="#aaa",
    )
    self.lbl_status.pack()

    self.card_palavra = ctk.CTkFrame(
        self.root, corner_radius=15, fg_color=self.COR_CARD
    )
    self.card_palavra.pack(pady=10, padx=40, fill="x")

    ctk.CTkLabel(
        self.card_palavra,
        text="Qual país tem essa bandeira?",
        font=ctk.CTkFont(size=14),
        text_color="#bbb",
    ).pack(pady=(12, 0))

    self.lbl_bandeira = tk.Label(
        self.card_palavra,
        bg=self.COR_CARD,
        borderwidth=0,
        highlightthickness=0,
    )
    self.lbl_bandeira.pack(pady=5)

    self.ent_resposta = ctk.CTkEntry(
        self.root,
        placeholder_text="Nome do país...",
        font=ctk.CTkFont(size=14),
        width=260,
        height=40,
        corner_radius=10,
        justify="center",
    )
    self.ent_resposta.pack(pady=10)
    self.ent_resposta.bind("<Return>", lambda event: self.verificar_resposta())

    self.btn_responder = ctk.CTkButton(
        self.root,
        text="Confirmar [Enter]",
        font=ctk.CTkFont(size=14, weight="bold"),
        fg_color="#e67e22",
        hover_color="#d35400",
        text_color="white",
        height=40,
        corner_radius=20,
        command=self.verificar_resposta,
    )
    self.btn_responder.pack(pady=5)

    self.lbl_feedback = ctk.CTkLabel(
        self.root, text="", font=ctk.CTkFont(size=15, weight="bold")
    )
    self.lbl_feedback.pack(pady=5)

  def proxima_pergunta(self):
    if self.rodada_atual > TOTAL_PERGUNTAS:
      self.finalizar_partida()
      return

    nome_atual = self.j1 if self.jogador_atual == 1 else self.j2
    self.lbl_turno.configure(text=f"Vez de: {nome_atual}")
    self.lbl_placar_parcial.configure(
        text=f"Placar: {self.j1} [{self.pontos_j1}] x [{self.pontos_j2}] {self.j2}"
    )

    if self.jogador_atual == 1:
      item_pergunta, fase_nome = self.perguntas_j1.pop()
    else:
      item_pergunta, fase_nome = self.perguntas_j2.pop()

    self.pergunta_atual = item_pergunta
    self.lbl_fase.configure(text=fase_nome)
    self.lbl_status.configure(
        text=f"Pergunta {self.rodada_atual} de {TOTAL_PERGUNTAS}"
    )

    self.lbl_bandeira.configure(
        image=self.imagens_bandeiras[self.pergunta_atual[0]], text=""
    )
    self.ent_resposta.configure(state="normal")
    self.btn_responder.configure(state="normal")
    self.ent_resposta.focus()

  def verificar_resposta(self):
    resposta_user = remover_acentos(self.ent_resposta.get().strip().lower())
    resposta_certa = self.pergunta_atual[1].lower()
    resposta_certa_sem_acento = remover_acentos(resposta_certa)

    self.ent_resposta.delete(0, tk.END)

    self.ent_resposta.configure(state="disabled")
    self.btn_responder.configure(state="disabled")

    if resposta_user == resposta_certa_sem_acento:
      if self.jogador_atual == 1:
        self.pontos_j1 += 1
      else:
        self.pontos_j2 += 1

      self.animar_feedback("#1b5e20", "CORRETO! +1 PONTO", "#EEE")
    else:
      self.animar_feedback(
          "#b71c1c",
          f"ERRADO! Era '{resposta_certa.title()}'",
          "#EEE",
      )

  def animar_feedback(self, cor_fundo, texto_feedback, cor_texto):
    self.root.configure(fg_color=cor_fundo)
    self.lbl_feedback.configure(text=texto_feedback, text_color=cor_texto)

    def restaurar():
      self.root.configure(fg_color=self.COR_FUNDO_PADRAO)
      self.lbl_feedback.configure(text="")

      if self.jogador_atual == 1:
        self.jogador_atual = 2
      else:
        self.jogador_atual = 1
        self.rodada_atual += 1

      self.proxima_pergunta()

    self.root.after(1500, restaurar)

  # --- TELA 3: RESULTADO FINAL COM FOGOS DE ARTIFÍCIO ---
  def finalizar_partida(self):
    self.limpar_tela()

    with open("pontuacoes.txt", "a", encoding="utf-8") as arq:
      arq.write(
          f"Bandeiras - {self.j1}: {self.pontos_j1} pts | {self.j2}:"
          f" {self.pontos_j2} pts\n"
      )

    self.canvas_fogos = tk.Canvas(
        self.root, bg=self.COR_FUNDO_PADRAO, highlightthickness=0
    )
    self.canvas_fogos.place(x=0, y=0, relwidth=1, relheight=1)

    frame_conteudo = ctk.CTkFrame(self.root, fg_color="transparent")
    frame_conteudo.pack(pady=20, fill="both", expand=True)

    ctk.CTkLabel(
        frame_conteudo,
        text="PLACAR FINAL",
        font=ctk.CTkFont(size=24, weight="bold"),
        text_color="#f1c40f",
    ).pack(pady=15)

    card = ctk.CTkFrame(
        frame_conteudo, corner_radius=15, fg_color=self.COR_CARD
    )
    card.pack(pady=10, padx=40, fill="both", expand=True)

    if self.pontos_j1 > self.pontos_j2:
      vencedor_txt = f"Parabéns, {self.j1} venceu!"
      houve_vencedor = True
    elif self.pontos_j2 > self.pontos_j1:
      vencedor_txt = f"Parabéns, {self.j2} venceu!"
      houve_vencedor = True
    else:
      vencedor_txt = "Tivemos um empate!"
      houve_vencedor = False

    ctk.CTkLabel(
        card,
        text=vencedor_txt,
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#2ecc71",
    ).pack(pady=20)

    ctk.CTkLabel(
        card,
        text=f"{self.j1}: {self.pontos_j1}/{TOTAL_PERGUNTAS} pontos\n{self.j2}: {self.pontos_j2}/{TOTAL_PERGUNTAS} pontos",
        font=ctk.CTkFont(size=16),
    ).pack(pady=10)

    ctk.CTkButton(
        card,
        text="Jogar Novamente",
        font=ctk.CTkFont(size=14, weight="bold"),
        fg_color="#27ae60",
        hover_color="#219653",
        height=40,
        corner_radius=20,
        command=self.criar_tela_inicio,
    ).pack(pady=25)

    if houve_vencedor:
      self.animacao_fogos_ativa = True
      self.particulas = []
      self.iniciar_fogos()

  def criar_explosao(self):
    cx = random.randint(50, 470)
    cy = random.randint(50, 300)
    cores = [
        "#f1c40f",
        "#e74c3c",
        "#3498db",
        "#2ecc71",
        "#9b59b6",
        "#e67e22",
        "#ffffff",
    ]
    cor = random.choice(cores)

    for _ in range(35):
      vx = random.uniform(-5, 5)
      vy = random.uniform(-6, 3)
      tamanho = random.randint(3, 6)
      id_p = self.canvas_fogos.create_oval(
          cx, cy, cx + tamanho, cy + tamanho, fill=cor, outline=""
      )
      self.particulas.append(
          {"id": id_p, "vx": vx, "vy": vy, "vida": random.randint(20, 35)}
      )

  def iniciar_fogos(self):
    if not self.animacao_fogos_ativa:
      return

    if random.random() < 0.25:
      self.criar_explosao()

    novas_particulas = []
    for p in self.particulas:
      self.canvas_fogos.move(p["id"], p["vx"], p["vy"])
      p["vy"] += 0.25
      p["vida"] -= 1

      if p["vida"] > 0:
        novas_particulas.append(p)
      else:
        self.canvas_fogos.delete(p["id"])

    self.particulas = novas_particulas
    self.root.after(40, self.iniciar_fogos)

  # --- TELA 4: HISTÓRICO ---
  def mostrar_historico(self):
    janela_hist = ctk.CTkToplevel(self.root)
    janela_hist.title("Histórico de Pontuações")
    janela_hist.geometry("400x350")
    janela_hist.grab_set()

    txt = ctk.CTkTextbox(
        janela_hist, font=ctk.CTkFont(size=13), corner_radius=10
    )
    txt.pack(expand=True, fill="both", padx=15, pady=15)

    try:
      with open("pontuacoes.txt", "r", encoding="utf-8") as arq:
        conteudo = arq.read()
        txt.insert("1.0", conteudo if conteudo else "Nenhum histórico salvo.")
    except FileNotFoundError:
      txt.insert("1.0", "Nenhum histórico encontrado ainda.")

    txt.configure(state="disabled")


if __name__ == "__main__":
  root = ctk.CTk()
  app = JogoBandeirasApp(root)
  root.mainloop()