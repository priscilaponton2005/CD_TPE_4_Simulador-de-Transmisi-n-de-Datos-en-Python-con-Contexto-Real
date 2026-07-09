import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time

class SimuladorContextoRealUNEMI:
    def __init__(self, root):
        self.root = root
        self.root.title("PROYECTO: COMUNICACIÓN DE DATOS - UNEMI")
        
        # --- CONTROL DE ESTADO DE ANIMACIÓN ---
        self.en_pausa = False
        self.transmitiendo = False
        
        # --- FORZAR INICIO MAXIMIZADO ---
        self.root.state('zoomed') 
        self.root.configure(bg="#BED6E0") # Fondo general: Starlight Blue
        
        # --- BASE DE DATOS DE CONTEXTO REAL CON LOS 5 ESCENARIOS SOLICITADOS ---
        self.detalles_reales = [
            {
                "ejemplo": "WHATSAPP (WI-FI)",
                "explicacion": "Los bits de tu mensaje se modulan en ondas de radio de 2.4GHz. Aquí aplicas el Subtema 1: Datos digitales viajando en señales analógicas.",
                "teoria": "Teorema de Nyquist: Define la tasa máxima de bits en el aire."
            },
            {
                "ejemplo": "NETFLIX (FIBRA ÓPTICA)",
                "explicacion": "La luz se enciende y apaga (bits) para viajar por el vidrio. Es una señal periódica (Subtema 2) de altísima frecuencia.",
                "teoria": "Ancho de Banda: Es masivo, permitiendo video en 4K sin retrasos."
            },
            {
                "ejemplo": "LLAMADA CELULAR",
                "explicacion": "Tu voz (analógica) se digitaliza para procesarse y luego vuelve a ser onda para salir por la antena.",
                "teoria": "Relación Señal/Ruido (SNR): Si hay interferencia, la calidad de voz baja."
            },
            {
                "ejemplo": "CONTROL DE TV (INFRARROJO)",
                "explicacion": "Pulsas un botón (dato discreto) y un LED emite ráfagas de luz invisible que el TV interpreta.",
                "teoria": "Codificación: Cada botón tiene una secuencia de bits única."
            },
            {
                "ejemplo": "TRANSACCIÓN CAJERO (ATM)",
                "explicacion": "Tus datos bancarios viajan encriptados por cables de cobre usando módems DSL.",
                "teoria": "Ciberseguridad: Como dice el PDF, es una vulnerabilidad compartida en redes públicas."
            }
        ]

        # 1. ENCABEZADO (Fondo: Prussian Blue, Texto Principal: Starlight Blue)
        header = tk.Frame(root, bg="#003153", pady=20)
        header.pack(side=tk.TOP, fill=tk.X)
        tk.Label(header, text="UNIVERSIDAD ESTATAL DE MILAGRO", font=("Helvetica", 18, "bold"), bg="#003153", fg="#BED6E0").pack()
        tk.Label(header, text="FACULTAD DE CIENCIAS E INGENIERÍA - TECNOLOGÍAS DE LA INFORMACIÓN", font=("Helvetica", 12, "bold"), bg="#003153", fg="#3B8AB1").pack(pady=4)
        tk.Label(header, text="MODALIDAD EN LÍNEA - GRUPO D", font=("Helvetica", 10, "italic", "bold"), bg="#003153", fg="#BED6E0").pack()

        # 2. PIE DE PÁGINA (Fondo: Prussian Blue)
        footer = tk.Frame(root, bg="#003153", pady=15, padx=40)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        
        footer.columnconfigure(0, weight=4)
        footer.columnconfigure(1, weight=3)
        footer.columnconfigure(2, weight=3)

        # --- COLUMNA 1: AUTORES ---
        col_autores = tk.Frame(footer, bg="#003153")
        col_autores.grid(row=0, column=0, sticky="nw", padx=(0, 20))
        
        lbl_tit_autores = tk.Label(col_autores, text="AUTORES - GRUPO D", font=("Helvetica", 10, "bold"), bg="#003153", fg="#BED6E0")
        lbl_tit_autores.pack(anchor="w")
        
        linea1 = tk.Frame(col_autores, bg="#3B8AB1", height=2)
        linea1.pack(fill=tk.X, pady=(2, 6))

        autores_lista = (
            "Gomez Gomez Angel Eduardo\n"
            "Jaime Vera Arelys Dayana\n"
            "Medina Silva Samuel Sebastian\n"
            "Pacheco Lamilla Jonathan Gabriel\n"
            "Pontón Peña Priscila Indira\n"
            "Remache Jimenez Diego Javier\n"
            "Zerna Rodríguez Jeanpierre Adrián"
        )
        tk.Label(col_autores, text=autores_lista, font=("Segoe UI", 9), bg="#003153", fg="#BED6E0", justify=tk.LEFT).pack(anchor="w")

        # --- COLUMNA 2: ASIGNATURA ---
        col_asignatura = tk.Frame(footer, bg="#003153")
        col_asignatura.grid(row=0, column=1, sticky="nw", padx=20)
        
        lbl_tit_asig = tk.Label(col_asignatura, text="ASIGNATURA", font=("Helvetica", 10, "bold"), bg="#003153", fg="#BED6E0")
        lbl_tit_asig.pack(anchor="w")
        
        linea2 = tk.Frame(col_asignatura, bg="#3B8AB1", height=2)
        linea2.pack(fill=tk.X, pady=(2, 6))
        
        tk.Label(col_asignatura, text="Interacción Humano-Computador", font=("Segoe UI", 9), bg="#003153", fg="#BED6E0", justify=tk.LEFT).pack(anchor="w")

        # --- COLUMNA 3: DOCENTE ---
        col_docente = tk.Frame(footer, bg="#003153")
        col_docente.grid(row=0, column=2, sticky="nw", padx=(20, 0))
        
        lbl_tit_doc = tk.Label(col_docente, text="DOCENTE", font=("Helvetica", 10, "bold"), bg="#003153", fg="#BED6E0")
        lbl_tit_doc.pack(anchor="w")
        
        linea3 = tk.Frame(col_docente, bg="#3B8AB1", height=2)
        linea3.pack(fill=tk.X, pady=(2, 6))
        
        tk.Label(col_docente, text="MSc. Alex Armando Avila Coello", font=("Segoe UI", 9), bg="#003153", fg="#BED6E0", justify=tk.LEFT).pack(anchor="w")

        # 3. CUERPO CENTRAL (Fondo: Starlight Blue)
        main_body = tk.Frame(root, bg="#BED6E0")
        main_body.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        main_body.columnconfigure(0, weight=1)
        main_body.columnconfigure(1, weight=5)
        main_body.rowconfigure(0, weight=1)

        # --- ÁREA IZQUIERDA: PANEL DE CONTROL (Fondo: Wave Ride)
        left_container = tk.Frame(main_body, bg="#3B8AB1", bd=1, relief=tk.RIDGE, padx=15, pady=25)
        left_container.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        left_container.columnconfigure(0, weight=1)

        control_frame = tk.LabelFrame(left_container, text=" PANEL DE CONTROL ", font=("Helvetica", 11, "bold"), bg="#3B8AB1", fg="#003153", padx=10, pady=20)
        control_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        tk.Label(control_frame, text="Mensaje a enviar:", font=("Helvetica", 12, "bold"), bg="#3B8AB1", fg="#003153", anchor="w").pack(fill=tk.X, pady=(5, 5))

        self.entry_msg = tk.Entry(control_frame, font=("Arial", 16), width=12, justify='center', bg="#ffffff", fg="#003153", insertbackground="black")
        self.entry_msg.pack(fill=tk.X, pady=(0, 35))
        self.entry_msg.insert(0, "UNEMI")

        # Botones de control
        self.btn_tx = tk.Button(control_frame, text="TRANSMITIR Y ANALIZAR", command=self.transmitir, bg="#003153", font=("Helvetica", 11, "bold"), fg="#BED6E0", pady=8, activebackground="#3B8AB1")
        self.btn_tx.pack(fill=tk.X, pady=5)
        
        # Subcontenedor para controles de pausa
        pause_frame = tk.Frame(control_frame, bg="#3B8AB1")
        pause_frame.pack(fill=tk.X, pady=5)
        pause_frame.columnconfigure(0, weight=1)
        pause_frame.columnconfigure(1, weight=1)
        
        self.btn_pausa = tk.Button(pause_frame, text="PAUSA", command=self.pausar, bg="#003153", font=("Helvetica", 10, "bold"), fg="#BED6E0", state=tk.DISABLED, pady=6)
        self.btn_pausa.grid(row=0, column=0, sticky="ew", padx=(0, 2))
        
        self.btn_continuar = tk.Button(pause_frame, text="CONTINUAR", command=self.continuar, bg="#003153", font=("Helvetica", 10, "bold"), fg="#BED6E0", state=tk.DISABLED, pady=6)
        self.btn_continuar.grid(row=0, column=1, sticky="ew", padx=(2, 0))
        
        tk.Button(control_frame, text="RESET", command=self.reset, bg="#3B8AB1", fg="#003153", font=("Helvetica", 11, "bold"), pady=8, relief=tk.GROOVE).pack(fill=tk.X, pady=15)

        # --- ÁREA DERECHA: SEÑALES Y MONITOR (Fondo: Starlight Blue)
        right_container = tk.Frame(main_body, bg="#BED6E0")
        right_container.grid(row=0, column=1, sticky="nsew")
        right_container.columnconfigure(0, weight=1)
        right_container.rowconfigure(1, weight=3)
        right_container.rowconfigure(3, weight=3)

        # Marco de Conceptos Clave
        diff_frame = tk.Frame(right_container, bg="#3B8AB1", pady=6, bd=1, relief=tk.RIDGE)
        diff_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        tk.Label(diff_frame, text="CONCEPTOS CLAVE DE LA UNIDAD 3", font=("Helvetica", 10, "bold"), bg="#3B8AB1", fg="#003153").pack()
        info_txt = "Señal Digital: Discreta (0,1) | Señal Analógica: Continua (Ondas) | Teorema de Nyquist: C = 2 * B * log2(L)"
        tk.Label(diff_frame, text=info_txt, font=("Helvetica", 9), bg="#3B8AB1", fg="#003153").pack()

        # Configuración de Gráficos de Señales (Matplotlib)
        self.fig, (self.ax_dig, self.ax_ana) = plt.subplots(2, 1, figsize=(7, 4.0))
        self.fig.patch.set_facecolor('#BED6E0')
        self.fig.subplots_adjust(hspace=0.5, top=0.9, bottom=0.15)
        for ax in [self.ax_dig, self.ax_ana]:
            ax.set_facecolor('#3B8AB1')        
            ax.tick_params(colors='#003153', labelsize=8)
            ax.title.set_color('#003153')

        self.canvas = FigureCanvasTkAgg(self.fig, master=right_container)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew", pady=(0, 5))

        # Monitor de Tráfico
        tk.Label(right_container, text="MONITOR DE TRÁFICO EN TIEMPO REAL", font=("Helvetica", 9, "bold"), bg="#BED6E0", fg="#003153").grid(row=2, column=0, sticky="w")
        
        self.consola = tk.Text(right_container, bg="#BED6E0", fg="#003153", font=("Consolas", 10), padx=10, pady=10, wrap=tk.WORD, height=10, highlightbackground="#3B8AB1", bd=1)
        self.consola.grid(row=3, column=0, sticky="nsew")

        # Configuración de tags en consola
        self.consola.tag_config("ESCENARIO", foreground="#003153", font=("Consolas", 10, "bold"))  
        self.consola.tag_config("APLICACIÓN", foreground="#003153")                               
        self.consola.tag_config("TEORÍA U3", foreground="#003153", font=("Consolas", 10, "italic"))                             
        self.consola.tag_config("SISTEMA", foreground="#003153", font=("Consolas", 10, "bold"))    
        self.consola.tag_config("TEXTO", foreground="#003153")                                     

    def log_color(self, tag, msg):
        self.consola.insert(tk.END, f"[{tag}] ", tag)
        self.consola.insert(tk.END, f"{msg}\n", "TEXTO")
        self.consola.see(tk.END)
        self.root.update()

    def pausar(self):
        if self.transmitiendo and not self.en_pausa:
            self.en_pausa = True
            self.btn_pausa.config(state=tk.DISABLED)
            self.btn_continuar.config(state=tk.NORMAL)
            self.log_color("SISTEMA", "Transmisión pausada por el usuario...")

    def continuar(self):
        if self.transmitiendo and self.en_pausa:
            self.en_pausa = False
            self.btn_pausa.config(state=tk.NORMAL)
            self.btn_continuar.config(state=tk.DISABLED)
            self.log_color("SISTEMA", "Reanudando transmisión de datos...")

    def reset(self):
        self.en_pausa = False
        self.transmitiendo = False
        self.ax_dig.clear()
        self.ax_ana.clear()
        self.canvas.draw()
        self.consola.delete(1.0, tk.END)
        self.btn_tx.config(state=tk.NORMAL)
        self.btn_pausa.config(state=tk.DISABLED)
        self.btn_continuar.config(state=tk.DISABLED)

    def transmitir(self):
        texto = self.entry_msg.get().upper()
        if not texto: return
        
        self.transmitiendo = True
        self.en_pausa = False
        self.btn_tx.config(state=tk.DISABLED)
        self.btn_pausa.config(state=tk.NORMAL)
        self.btn_continuar.config(state=tk.DISABLED)
        self.consola.delete(1.0, tk.END)
        
        i = 0
        while i < len(texto):
            # Si el usuario presionó Pausa, espera activamente procesando eventos gráficos
            if self.en_pausa:
                self.root.update()
                time.sleep(0.1)
                continue
                
            letra = texto[i]
            self.ax_dig.clear()
            self.ax_ana.clear()
            
            bits = [int(b) for b in format(ord(letra), '08b')]
            
            self.ax_dig.step(range(len(bits)), bits, where='post', color='#003153', lw=2)
            self.ax_dig.set_title(f"DOMINIO DIGITAL: Carácter '{letra}' procesado en CPU")
            self.ax_dig.set_ylim(-0.2, 1.2)

            t = np.linspace(0, len(bits), 1000)
            frecuencia = 5
            senal = np.sin(2 * np.pi * frecuencia * t) * np.repeat(bits, 1000 // len(bits))
            
            self.ax_ana.plot(t, senal, color='#003153', lw=1.5)
            self.ax_ana.set_title(f"MEDIO FÍSICO: Onda Analógica transportando '{letra}'")
            
            self.canvas.draw()
            
            detalle = self.detalles_reales[i % len(self.detalles_reales)]
            self.log_color("ESCENARIO", detalle['ejemplo'])
            self.log_color("APLICACIÓN", detalle['explicacion'])
            self.log_color("TEORÍA U3", detalle['teoria'])
            self.consola.insert(tk.END, "-"*55 + "\n", "TEXTO")
            self.consola.see(tk.END)
            
            # Retraso controlado que permite la interacción gráfica con la pausa
            for _ in range(20):
                if not self.en_pausa:
                    self.root.update()
                    time.sleep(0.1)
            
            i += 1

        self.log_color("SISTEMA", f"Mensaje '{texto}' recibido. Verificación de paridad OK.")
        self.transmitiendo = False
        self.btn_tx.config(state=tk.NORMAL)
        self.btn_pausa.config(state=tk.DISABLED)
        self.btn_continuar.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorContextoRealUNEMI(root)
    root.mainloop()
