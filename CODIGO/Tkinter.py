root = tk.Tk()
root.title("Proyecto Resistencia Eléctrica")
root.geometry("400x450")

tk.Label(root, text="Valor de la Resistencia (Ohmios):").pack(pady=5)
entry_valor = tk.Entry(root)
entry_valor.pack(pady=5)

tk.Label(root, text="Cantidad de resistencias (n):").pack(pady=5)
entry_n = tk.Entry(root)
entry_n.pack(pady=5)

tk.Button(root, text="Calcular", command=calcular_grafico).pack(pady=15)

# Visualización de grafica de colores
frame_colores = tk.Frame(root)
frame_colores.pack(pady=10)

lbl_color1 = tk.Label(frame_colores, width=10, height=2, borderwidth=2, relief="groove")
lbl_color1.grid(row=0, column=0, padx=5)
lbl_color2 = tk.Label(frame_colores, width=10, height=2, borderwidth=2, relief="groove")
lbl_color2.grid(row=0, column=1, padx=5)
lbl_color3 = tk.Label(frame_colores, width=10, height=2, borderwidth=2, relief="groove")
lbl_color3.grid(row=0, column=2, padx=5)

resultado_colores = tk.Label(root, text="")
resultado_colores.pack(pady=5)

resultado_sumas = tk.Label(root, text="", justify=tk.LEFT)
resultado_sumas.pack(pady=15)

root.mainloop()
