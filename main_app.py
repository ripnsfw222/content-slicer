import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
import windnd
from video_processor import VideoProcessor

# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class SmartVidPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Content-Slicer 🚀")
        self.root.geometry("800x600")
        
        # Variáveis
        self.video_path = ctk.StringVar()
        self.status_var = ctk.StringVar(value="Aguardando arquivo...")
        self.num_parts = ctk.StringVar(value="2")
        self.max_size = ctk.StringVar(value="25")
        
        # Instância do Processador
        self.processor = VideoProcessor()

        # Cores Personalizadas (Estilo Cyberpunk/Moderno)
        self.bg_color = "#1a1a1a"
        self.panel_color = "#2b2b2b"
        self.accent_color = "#7b2cbf"  # Roxo profundo
        self.accent_hover = "#9d4edd" # Roxo mais claro
        self.text_color = "#ffffff"
        
        # Forçar background escuro na janela principal
        self.root.configure(fg_color=self.bg_color)
        
        self.setup_ui()
        
        # Registrar o Drag and Drop com suporte a Unicode (importante para emojis/caracteres especiais)
        windnd.hook_dropfiles(self.root, func=self.on_drop, force_unicode=True)

    def on_drop(self, files):
        if not files:
            return
            
        # Pega o primeiro arquivo solto
        file_path = files[0]
        
        # O windnd com force_unicode=True já entrega strings Unicode prontas
        if isinstance(file_path, bytes):
            file_path = file_path.decode('utf-8', errors='ignore')

        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.mp4', '.mkv', '.avi', '.webm', '.mov']:
            self.video_path.set(file_path)
            self.status_var.set(f"Arquivo carregado: {os.path.basename(file_path)}")
            # self.btn_play.configure(state="normal") # Exemplo de reativar coisas
        else:
            messagebox.showwarning("Formato Inválido", 
                                 f"Por favor, solte um arquivo de vídeo válido!\n\nArquivo detectado: {os.path.basename(file_path)}")

    def setup_ui(self):
        # --- Layout Principal (Grid 1x2) ---
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # 1. Sidebar (Menu Lateral)
        self.sidebar_frame = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        # Logo / Título
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Content\nSlicer", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.txt_intro = ctk.CTkLabel(self.sidebar_frame, text="Ferramentas de Vídeo\nAutomatizadas", font=ctk.CTkFont(size=12), text_color="gray")
        self.txt_intro.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Botões da Sidebar (Ações Rápidas)
        # Random Highlights (6x20)
        self.btn_h1 = ctk.CTkButton(self.sidebar_frame, text="Destaques (6x20s)", 
                                    command=lambda: self.run_task(lambda: self.processor.random_highlights(self.video_path.get(), 6, 20)),
                                    fg_color=self.panel_color, hover_color=self.accent_color)
        self.btn_h1.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # Random Highlights (10x5)
        self.btn_h2 = ctk.CTkButton(self.sidebar_frame, text="Destaques Curtos (10x5s)", 
                                    command=lambda: self.run_task(lambda: self.processor.random_highlights(self.video_path.get(), 10, 5)),
                                    fg_color=self.panel_color, hover_color=self.accent_color)
        self.btn_h2.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # TikTok Highlight (Feature Premium)
        self.btn_tiktok = ctk.CTkButton(self.sidebar_frame, text="✨ Gerar TikTok ✨", 
                                       command=lambda: self.run_task(lambda: self.processor.tiktok_highlights(self.video_path.get(), status_callback=self.status_var.set)),
                                       fg_color=self.accent_color, hover_color=self.accent_hover)
        self.btn_tiktok.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        # Remove Audio
        self.btn_audio = ctk.CTkButton(self.sidebar_frame, text="Remover Áudio", 
                                      command=lambda: self.run_task(lambda: self.processor.remove_audio(self.video_path.get())),
                                      fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.btn_audio.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        # 2. Main Area (Área Principal)
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # File Selection Block
        self.file_frame = ctk.CTkFrame(self.main_frame)
        self.file_frame.pack(fill="x", pady=(0, 20))

        self.lbl_file = ctk.CTkLabel(self.file_frame, text="Arquivo Selecionado:", anchor="w")
        self.lbl_file.pack(fill="x", padx=15, pady=(15, 5))

        self.entry_file = ctk.CTkEntry(self.file_frame, textvariable=self.video_path, placeholder_text="Arraste um vídeo aqui ou clique em Selecionar...")
        self.entry_file.pack(fill="x", padx=15, pady=(0, 15))

        self.btn_select = ctk.CTkButton(self.file_frame, text="Selecionar Vídeo", command=self.select_file)
        self.btn_select.pack(side="right", padx=15, pady=(0, 15))

        # Split Options Block
        self.split_frame = ctk.CTkFrame(self.main_frame)
        self.split_frame.pack(fill="x", pady=10)

        self.lbl_split_title = ctk.CTkLabel(self.split_frame, text="Ferramentas de Corte", font=ctk.CTkFont(size=16, weight="bold"), anchor="w")
        self.lbl_split_title.pack(fill="x", padx=15, pady=15)

        # Grid para inputs de corte
        self.split_grid = ctk.CTkFrame(self.split_frame, fg_color="transparent")
        self.split_grid.pack(fill="x", padx=15, pady=(0, 15))

        # Dividir em Partes
        self.lbl_parts = ctk.CTkLabel(self.split_grid, text="Nº de Partes:")
        self.lbl_parts.grid(row=0, column=0, padx=5, sticky="w")
        
        self.entry_parts = ctk.CTkEntry(self.split_grid, textvariable=self.num_parts, width=60)
        self.entry_parts.grid(row=0, column=1, padx=5, sticky="w")
        
        self.btn_split_parts = ctk.CTkButton(self.split_grid, text="Cortar", width=80, 
                                            command=lambda: self.run_task(self.handle_split_parts))
        self.btn_split_parts.grid(row=0, column=2, padx=10, sticky="w")

        # Dividir por MB
        self.lbl_mb = ctk.CTkLabel(self.split_grid, text="Max MB:")
        self.lbl_mb.grid(row=1, column=0, padx=5, pady=10, sticky="w")
        
        self.entry_mb = ctk.CTkEntry(self.split_grid, textvariable=self.max_size, width=60)
        self.entry_mb.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        
        self.btn_split_mb = ctk.CTkButton(self.split_grid, text="Cortar por Tamanho", width=120, 
                                         command=lambda: self.run_task(self.handle_split_mb))
        self.btn_split_mb.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        # 3. Process Console (Logs) - Preenche o espaço vazio
        self.log_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.log_frame.pack(fill="both", expand=True, pady=10)
        
        self.lbl_log = ctk.CTkLabel(self.log_frame, text="Log de Processamento:", anchor="w", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_log.pack(fill="x", padx=15, pady=(5, 5))
        
        self.log_box = ctk.CTkTextbox(self.log_frame, font=ctk.CTkFont(family="Consolas", size=11), activate_scrollbars=True)
        self.log_box.pack(fill="both", expand=True, padx=15, pady=(0, 5))
        self.log_box.configure(state="disabled")

        # Status Footer
        self.status_label = ctk.CTkLabel(self.main_frame, textvariable=self.status_var, 
                                        font=ctk.CTkFont(size=12), text_color="gray")
        self.status_label.pack(side="bottom", fill="x", pady=(0, 10))

        # Progress Bar (Indeterminado)
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, height=10)
        self.progress_bar.pack(side="bottom", fill="x", padx=20, pady=(5, 10))
        self.progress_bar.set(0)

    def log_message(self, message):
        self.root.after(0, lambda: self._log_ui(message))
        
    def _log_ui(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"> {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mkv *.avi *.webm *.mov")])
        if file_path:
            self.video_path.set(file_path)
            self.status_var.set(f"Pronto: {os.path.basename(file_path)}")
            self.log_message(f"Arquivo selecionado: {file_path}")

    def run_task(self, task_func):
        if not self.video_path.get():
            messagebox.showwarning("Aviso", "Selecione um vídeo primeiro!")
            return
        
        self.log_message("Iniciando tarefa...")
        self.btn_select.configure(state="disabled")
        self.progress_bar.start() 
        self.status_var.set("Processando...")
        
        # Thread Wrapper para capturar retornos e erros
        def thread_target():
            try:
                result = task_func()
                if result:
                    self.finish_task(result)
                else:
                    self.finish_task("Tarefa concluída!") # Fallback msg
            except Exception as e:
                self.error_task(str(e))

        thread = threading.Thread(target=thread_target, daemon=True)
        thread.start()

    def finish_task(self, message):
        self.root.after(0, lambda: self._finish_ui(message))

    def _finish_ui(self, message):
        self.progress_bar.stop()
        self.progress_bar.set(1) 
        self.status_var.set("Concluído!")
        self.log_message(f"SUCESSO: {message}")
        messagebox.showinfo("Sucesso", message)
        self.btn_select.configure(state="normal")
        self.progress_bar.set(0)

    def error_task(self, message):
        self.root.after(0, lambda: self._error_ui(message))

    def _error_ui(self, message):
        self.progress_bar.stop()
        self.progress_bar.set(0)
        self.status_var.set("Erro!")
        self.log_message(f"ERRO: {message}")
        messagebox.showerror("Erro", f"Ocorreu um erro: {message}")
        self.btn_select.configure(state="normal")

    # Wrappers para pegar inputs da UI antes de chamar a lógica
    def handle_split_parts(self):
        parts = int(self.num_parts.get())
        return self.processor.split_video(self.video_path.get(), parts)

    def handle_split_mb(self):
        mb = float(self.max_size.get())
        return self.processor.split_by_size(self.video_path.get(), mb, status_callback=lambda msg: self.root.after(0, lambda: self.status_var.set(msg)))

if __name__ == "__main__":
    root = ctk.CTk()
    app = SmartVidPro(root)
    root.mainloop()
