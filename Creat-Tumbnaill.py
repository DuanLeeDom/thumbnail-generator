import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
import os

class ThumbnailGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Thumbnail Generator")

        self.gameplay_path = ""
        self.webcam_path = ""
        self.webcam_posicao = tk.StringVar()
        self.webcam_posicao.set("Direita")  # Valor padrão

        self.label_gameplay = tk.Label(root, text="Gameplay:")
        self.label_gameplay.grid(row=0, column=0)

        self.label_webcam = tk.Label(root, text="Webcam:")
        self.label_webcam.grid(row=1, column=0)

        self.label_posicao = tk.Label(root, text="Posição da Webcam:")
        self.label_posicao.grid(row=2, column=0)

        self.entry_gameplay = tk.Entry(root, state="disabled", width=30)
        self.entry_gameplay.grid(row=0, column=1)

        self.entry_webcam = tk.Entry(root, state="disabled", width=30)
        self.entry_webcam.grid(row=1, column=1)

        self.radio_direita = tk.Radiobutton(root, text="Direita", variable=self.webcam_posicao, value="Direita")
        self.radio_direita.grid(row=2, column=1)

        self.radio_esquerda = tk.Radiobutton(root, text="Esquerda", variable=self.webcam_posicao, value="Esquerda")
        self.radio_esquerda.grid(row=2, column=2)

        self.button_gameplay = tk.Button(root, text="Selecionar Gameplay", command=self.selecionar_gameplay)
        self.button_gameplay.grid(row=0, column=2)

        self.button_webcam = tk.Button(root, text="Selecionar Webcam", command=self.selecionar_webcam)
        self.button_webcam.grid(row=1, column=2)

        self.button_gerar_thumbnail = tk.Button(root, text="Gerar Thumbnail e Abrir no Visualizador Padrão", command=self.gerar_e_visualizar_thumbnail)
        self.button_gerar_thumbnail.grid(row=3, column=0, columnspan=3)

        self.cor_divisoria = tk.StringVar()
        self.cor_divisoria.set("#FFFFFF")  # Cor padrão da divisória

        self.label_cor_divisoria = tk.Label(root, text="Cor da Divisória:")
        self.label_cor_divisoria.grid(row=4, column=0)

        self.entry_cor_divisoria = tk.Entry(root, textvariable=self.cor_divisoria, width=7)
        self.entry_cor_divisoria.grid(row=4, column=1)

        self.label_tamanho_thumbnail = tk.Label(root, text="Tamanho da Thumbnail (px):")
        self.label_tamanho_thumbnail.grid(row=5, column=0)

        self.tamanho_thumbnail = tk.IntVar()
        self.tamanho_thumbnail.set(720)  # Tamanho padrão da Thumbnail

        self.entry_tamanho_thumbnail = tk.Entry(root, textvariable=self.tamanho_thumbnail, width=7)
        self.entry_tamanho_thumbnail.grid(row=5, column=1)

    def selecionar_gameplay(self):
        self.gameplay_path = filedialog.askopenfilename(title="Selecione a imagem da Gameplay", filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.gif")])
        self.entry_gameplay.config(state="normal")
        self.entry_gameplay.delete(0, tk.END)
        self.entry_gameplay.insert(0, self.gameplay_path)
        self.entry_gameplay.config(state="disabled")

    def selecionar_webcam(self):
        self.webcam_path = filedialog.askopenfilename(title="Selecione a imagem da Webcam", filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.gif")])
        self.entry_webcam.config(state="normal")
        self.entry_webcam.delete(0, tk.END)
        self.entry_webcam.insert(0, self.webcam_path)
        self.entry_webcam.config(state="disabled")

    def gerar_e_visualizar_thumbnail(self):
        if self.gameplay_path and self.webcam_path:
            thumbnail = self.criar_thumbnail(self.gameplay_path, self.webcam_path)
            thumbnail_path = "thumbnail.jpg"
            thumbnail.save(thumbnail_path, "JPEG")
            self.visualizar_thumbnail(thumbnail_path)

    def criar_thumbnail(self, gameplay_path, webcam_path):
        gameplay = Image.open(gameplay_path)
        webcam = Image.open(webcam_path)

        nova_largura = int(gameplay.width * 0.6)
        nova_altura_webcam = gameplay.height  # Defina a altura da webcam como a altura da gameplay diretamente

        # Redimensionar a webcam mantendo a proporção
        webcam = webcam.resize((nova_largura, int(webcam.height * (nova_largura / webcam.width))))

        # Certificar-se de que ambas as imagens tenham o mesmo tamanho
        webcam = webcam.resize((nova_largura, nova_altura_webcam))
        
        largura_total = gameplay.width + nova_largura
        altura_total = max(gameplay.height, nova_altura_webcam)

        # Criar uma nova imagem para a thumbnail
        thumbnail = Image.new("RGB", (largura_total, altura_total), (255, 255, 255))

        # Colar a gameplay na imagem thumbnail
        thumbnail.paste(gameplay, (0, 0))

        # Adicionar a divisória na cor especificada
        linha_x = gameplay.width
        cor_divisoria = self.cor_divisoria.get()
        draw = ImageDraw.Draw(thumbnail)
        draw.line([(linha_x, 0), (linha_x, altura_total)], fill=cor_divisoria, width=5)

        # Colar a webcam na posição especificada
        if self.webcam_posicao.get() == "Direita":
            thumbnail.paste(webcam, (linha_x, (altura_total - nova_altura_webcam) // 2))
        else:
            thumbnail.paste(webcam, (0, (altura_total - nova_altura_webcam) // 2))

        # Redimensionar para o tamanho especificado
        tamanho_thumbnail = self.tamanho_thumbnail.get()
        thumbnail = thumbnail.resize((1280, tamanho_thumbnail))

        return thumbnail

    def visualizar_thumbnail(self, imagem_path):
        os.system(f'start {imagem_path}')

if __name__ == '__main__':
    root = tk.Tk()
    app = ThumbnailGenerator(root)
    root.mainloop()