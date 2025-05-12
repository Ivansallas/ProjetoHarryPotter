import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import os

if not os.path.exists("participantes"):
    os.makedirs("participantes")

quiz = [
    {
        "pergunta": "O que você mais valoriza?",
        "opcoes": {
            "Coragem": "Grifinória",
            "Ambição": "Sonserina",
            "Sabedoria": "Corvinal",
            "Lealdade": "Lufa-Lufa",
        },
    },
    {
        "pergunta": "Qual animal você prefere?",
        "opcoes": {
            "Leão": "Grifinória",
            "Serpente": "Sonserina",
            "Águia": "Corvinal",
            "Texugo": "Lufa-Lufa",
        },
    },
    {
        "pergunta": "Qual matéria você mais gostaria de estudar?",
        "opcoes": {
            "Feitiços": "Grifinória",
            "Poções": "Sonserina",
            "Astronomia": "Corvinal",
            "Herbologia": "Lufa-Lufa",
        },
    },
]

respostas = []
pontos = {"Grifinória": 0, "Sonserina": 0, "Corvinal": 0, "Lufa-Lufa": 0}
pergunta_atual = 0


def iniciar_quiz():
    global respostas, pontos, pergunta_atual
    nome = entry_nome.get().strip()
    if not nome:
        messagebox.showwarning("Aviso", "Digite o nome do participante.")
        return
    respostas = []
    pontos.update({chave: 0 for chave in pontos})
    pergunta_atual = 0
    entry_nome.config(state="disabled")
    btn_iniciar.config(state="disabled")
    mostrar_pergunta()


def mostrar_pergunta():
    global pergunta_atual
    frame_quiz.pack(pady=10)
    pergunta = quiz[pergunta_atual]
    lbl_pergunta.config(text=pergunta["pergunta"])
    for widget in frame_opcoes.winfo_children():
        widget.destroy()
    for texto, casa in pergunta["opcoes"].items():
        btn = tk.Button(
            frame_opcoes,
            text=texto,
            font=("Georgia", 12, "bold"),
            bg="#3A3A3C",
            fg="white",
            width=20,
            relief="raised",
            command=lambda c=casa: responder(c),
        )
        btn.pack(pady=5)


def responder(casa):
    global pergunta_atual
    pontos[casa] += 1
    pergunta_atual += 1
    if pergunta_atual < len(quiz):
        mostrar_pergunta()
    else:
        frame_quiz.pack_forget()
        capturar_imagem()


def capturar_imagem():
    nome = entry_nome.get().strip()
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Captura de Imagem - Pressione Espaço")
    while True:
        ret, frame = cam.read()
        cv2.imshow("Captura de Imagem - Pressione Espaço", frame)
        key = cv2.waitKey(1)
        if key % 256 == 32:
            img_path = f"participantes/{nome}.png"
            cv2.imwrite(img_path, frame)
            break
    cam.release()
    cv2.destroyAllWindows()
    mostrar_resultado(nome, img_path)


def mostrar_resultado(nome, img_path):
    casa_final = max(pontos, key=pontos.get)
    with open("participantes/dados.txt", "a") as f:
        f.write(f"{nome} - {casa_final}\n")
    img = Image.open(img_path)
    img = img.resize((200, 200))
    photo = ImageTk.PhotoImage(img)
    img_label.config(image=photo)
    img_label.image = photo
    messagebox.showinfo(
        "Chapéu Seletor", f"{nome}, você foi selecionado para a casa: {casa_final}!"
    )


def mostrar_ranking():
    rank_window = tk.Toplevel()
    rank_window.title("Ranking dos Participantes")
    rank_window.geometry("600x500")
    rank_window.configure(bg="#1E1E2F")
    tk.Label(
        rank_window,
        text="🏆 Ranking dos Participantes",
        font=("Georgia", 16, "bold"),
        bg="#1E1E2F",
        fg="gold",
    ).pack(pady=10)
    canvas = tk.Canvas(rank_window, bg="#1E1E2F")
    scrollbar = tk.Scrollbar(rank_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#1E1E2F")
    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    contadores = {"Grifinória": 0, "Sonserina": 0, "Corvinal": 0, "Lufa-Lufa": 0}
    if os.path.exists("participantes/dados.txt"):
        with open("participantes/dados.txt", "r") as f:
            linhas = f.readlines()
        for linha in linhas:
            if "-" not in linha:
                continue
            nome, casa = [parte.strip() for parte in linha.strip().split("-")]
            contadores[casa] += 1
            img_path = f"participantes/{nome}.png"
            frame = tk.Frame(
                scrollable_frame, bg="#2C2C3A", bd=1, relief="solid", padx=10, pady=10
            )
            frame.pack(pady=5, padx=10, fill="x")
            if os.path.exists(img_path):
                img = Image.open(img_path)
                img = img.resize((60, 60))
                photo = ImageTk.PhotoImage(img)
                lbl_img = tk.Label(frame, image=photo, bg="#2C2C3A")
                lbl_img.image = photo
                lbl_img.pack(side="left", padx=10)
            info = tk.Label(
                frame,
                text=f"{nome} - {casa}",
                font=("Arial", 12),
                fg="white",
                bg="#2C2C3A",
            )
            info.pack(side="left")
    total_frame = tk.Frame(rank_window, pady=10, bg="#1E1E2F")
    total_frame.pack()
    for casa, count in contadores.items():
        tk.Label(
            total_frame,
            text=f"{casa}: {count} participantes",
            font=("Arial", 12, "bold"),
            bg="#1E1E2F",
            fg="white",
        ).pack()


# Interface principal
root = tk.Tk()
root.title("Chapéu Seletor - Hogwarts")
root.geometry("600x600")
root.configure(bg="#1E1E2F")

tk.Label(
    root,
    text="🏰 Bem-vindo à Seleção de Hogwarts!",
    font=("Georgia", 18, "bold"),
    fg="gold",
    bg="#1E1E2F",
).pack(pady=10)

tk.Label(
    root, text="Digite seu nome:", font=("Arial", 14), bg="#1E1E2F", fg="white"
).pack(pady=10)
entry_nome = tk.Entry(root, font=("Arial", 14), justify="center")
entry_nome.pack(pady=5)

btn_iniciar = tk.Button(
    root,
    text="Iniciar Quiz",
    font=("Arial", 12, "bold"),
    command=iniciar_quiz,
    bg="#800000",
    fg="white",
    relief="raised",
    bd=4,
)
btn_iniciar.pack(pady=20)

btn_rank = tk.Button(
    root,
    text="Mostrar Rank",
    font=("Arial", 12, "bold"),
    command=mostrar_ranking,
    bg="#FFD700",
    fg="black",
    relief="raised",
    bd=4,
)
btn_rank.pack(pady=20)

frame_quiz = tk.Frame(root, bg="#1E1E2F")
lbl_pergunta = tk.Label(
    frame_quiz,
    text="",
    font=("Arial", 14, "bold"),
    wraplength=400,
    justify="center",
    bg="#1E1E2F",
    fg="white",
)
lbl_pergunta.pack(pady=10)
frame_opcoes = tk.Frame(frame_quiz, bg="#1E1E2F")
frame_opcoes.pack()

img_label = tk.Label(root, bg="#1E1E2F")
img_label.pack(pady=20)

root.mainloop()
