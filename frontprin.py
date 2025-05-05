import tkinter as tk
from tkinter import messagebox
from tkinter import Toplevel, Scrollbar, Text
from backendcomp import Usuario, Gerente, Administrador, Empleado, Menu, Pedido, Inventario
import traceback 
import os


class VentanaInicio:
    def __init__(self, root):
        self.root = root
        self.root.title("Cafetería")
        self.root.geometry("800x800")
        self.root.config(bg="#F2EAD3")

        tk.Label(root, text="Bienvenido", font=("Arial", 14, "bold"), bg="#F2EAD3", fg="#4B3832").pack(pady=20)

        estilo_boton = {"width": 25, "bg": "#A67B5B", "fg": "white", "activebackground": "#8C5E3C", "font": ("Arial", 10, "bold")}

        tk.Button(root, text="Gerente", command=self.abrir_gerente, **estilo_boton).pack(pady=5)
        tk.Button(root, text="Administrador", command=self.abrir_admin, **estilo_boton).pack(pady=5)
        tk.Button(root, text="Empleado", command=self.abrir_empleado, **estilo_boton).pack(pady=5)
        tk.Button(root, text="Salir", command=root.quit, **estilo_boton).pack(pady=20)

    def abrir_gerente(self):
        self.root.destroy()
        root = tk.Tk()
        Ventgeren(root, self.volver_inicio)
        root.mainloop()

    def abrir_admin(self):
        self.root.destroy()
        root = tk.Tk()
        Ventadmin(root, self.volver_inicio)
        root.mainloop()

    def volver_inicio(self):
        root = tk.Tk()
        VentanaInicio(root)
        root.mainloop()

    def abrir_empleado(self):
        try:
            self.root.withdraw()
            self.empleado_root = tk.Tk()
            Ventemple(self.empleado_root, self.root)
            self.empleado_root.protocol("WM_DELETE_WINDOW", self.volver_a_inicio)
            self.empleado_root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir Empleado: {e}\n{traceback.format_exc()}")

    def volver_a_inicio(self):
        try:
            self.empleado_root.destroy()
            self.root.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"Error al volver a Inicio: {e}\n{traceback.format_exc()}")


class Ventgeren:
    def __init__(self, root, volver_inicio):
        self.root = root
        self.root.title("Gerente")
        self.root.geometry("600x600")
        self.gerente = Gerente("Gerente", "Gerecafe123")
        self.volver_inicio = volver_inicio

        Usuario.cargar_usuarios()
        Pedido.guardar_pedidos()

        tk.Label(root, text="Pedidos realizados", font=("Arial", 12, "bold")).pack()
        self.lista_pedidos = tk.Listbox(root, width=70, height=10)
        self.lista_pedidos.pack(pady=10)

        for p in Pedido.lista_pedidos:
            self.lista_pedidos.insert("end", f"#{p.id} - Cliente: {p.cliente} - Total: ${p.total():.2f}")

        tk.Label(root, text="Agregar usuario", font=("Arial", 12, "bold")).pack(pady=10)

        self.nuevo_nombre = tk.Entry(root)
        self.nuevo_nombre.insert(0, "Nombre")
        self.nuevo_nombre.pack()

        self.nuevo_rol = tk.Entry(root)
        self.nuevo_rol.insert(0, "Rol (Gerente, Administrador, Empleado)")
        self.nuevo_rol.pack()

        self.nuevo_pass = tk.Entry(root)
        self.nuevo_pass.insert(0, "Contraseña")
        self.nuevo_pass.pack()

        tk.Button(root, text="Agregar", command=self.agregar_usuario).pack(pady=5)

        self.nombre_eliminar = tk.Entry(root)
        self.nombre_eliminar.insert(0, "Nombre a eliminar")
        self.nombre_eliminar.pack()

        tk.Button(root, text="Eliminar usuario", command=self.eliminar_usuario).pack(pady=5)

        tk.Label(root, text="Modificar stock", font=("Arial", 12, "bold")).pack(pady=10)

        self.ingrediente_mod = tk.Entry(root)
        self.ingrediente_mod.insert(0, "Ingrediente")
        self.ingrediente_mod.pack()

        self.cantidad_mod = tk.Entry(root)
        self.cantidad_mod.insert(0, "Nuevo stock")
        self.cantidad_mod.pack()

        tk.Button(root, text="Actualizar stock", command=self.modificar_stock).pack(pady=5)

    def agregar_usuario(self):
        try:
            nombre = self.nuevo_nombre.get()
            rol = self.nuevo_rol.get()
            clave = self.nuevo_pass.get()
            self.gerente.agregar_usuario(nombre, rol, clave)
            messagebox.showinfo("Éxito", "Usuario agregado.")
        except:
            messagebox.showerror("Error", "Error al agregar usuario.")

    def eliminar_usuario(self):
        nombre = self.nombre_eliminar.get()
        self.gerente.eliminar_usuario(nombre)

    def modificar_stock(self):
        ing = self.ingrediente_mod.get()
        try:
            cant = int(self.cantidad_mod.get())
            self.gerente.modificar_stock(ing, cant)
            messagebox.showinfo("Éxito", "Stock actualizado.")
        except:
            messagebox.showerror("Error", "Cantidad inválida.")

    def salir(self):
        tk.Button(root, text="Salir", command=self.salir).pack(pady=5)

class Ventadmin:
    def __init__(self, root, volver_a_inicio):
        self.root = root
        self.root.title("Administrador")
        self.root.geometry("600x500")
        self.admin = Administrador("admin", "admin123")
        self.volver_a_inicio = volver_a_inicio
        self.carrito = []

        Menu.cargar_menu()
        Inventario.cargar_stock()
 
        tk.Label(root, text="Agregar producto al menú", font=("Arial", 12, "bold")).pack(pady=10)

        self.entrada_nombre = tk.Entry(root)
        self.entrada_nombre.insert(0, "Nombre del producto")
        self.entrada_nombre.pack()

        self.entrada_precio = tk.Entry(root)
        self.entrada_precio.insert(0, "Precio")
        self.entrada_precio.pack()

        self.entrada_ingredientes = tk.Entry(root)
        self.entrada_ingredientes.insert(0, "Ingredientes separados por coma")
        self.entrada_ingredientes.pack()

        self.entrada_opciones = tk.Entry(root)
        self.entrada_opciones.insert(0, "Opciones (opcional)")
        self.entrada_opciones.pack()

        self.seccion = tk.StringVar()
        self.categoria = tk.StringVar()

        tk.Label(root, text="Sección:").pack()
        tk.Entry(root, textvariable=self.seccion).pack()

        tk.Label(root, text="Categoría:").pack()
        tk.Entry(root, textvariable=self.categoria).pack()

        tk.Button(root, text="Agregar producto", command=self.agregar_producto).pack(pady=10)

        tk.Label(root, text="Modificar stock", font=("Arial", 12, "bold")).pack(pady=20)

        self.ingrediente_stock = tk.Entry(root)
        self.ingrediente_stock.insert(0, "Nombre del ingrediente")
        self.ingrediente_stock.pack()

        self.nuevo_stock = tk.Entry(root)
        self.nuevo_stock.insert(0, "Nuevo stock")
        self.nuevo_stock.pack()

        tk.Button(root, text="Actualizar stock", command=self.actualizar_stock).pack(pady=10)

    def agregar_producto(self):
        try:
            nombre = self.entrada_nombre.get()
            precio = float(self.entrada_precio.get())
            ingredientes = [i.strip() for i in self.entrada_ingredientes.get().split(",")]
            opciones = [o.strip() for o in self.entrada_opciones.get().split(",") if o.strip()]
            seccion = self.seccion.get()
            categoria = self.categoria.get()

            producto_dict = {"id": 59, "nombre": nombre, "precio": precio, "ingredientes": ingredientes, "opciones": opciones}

            self.admin.agregar_producto(seccion, categoria, producto_dict)
            messagebox.showinfo("Éxito", "Producto agregado al menú.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar: {e}")

    def actualizar_stock(self):
        ingrediente = self.ingrediente_stock.get()
        try:
            cantidad = int(self.nuevo_stock.get())
            self.admin.actualizar_stock(ingrediente, cantidad)
            messagebox.showinfo("Éxito", "Stock actualizado.")
        except:
            messagebox.showerror("Error", "Cantidad inválida.")


class Ventemple:
    def __init__(self, root, parent_root): 
        try:
            self.root = root
            self.parent_root = parent_root
            self.root.title("Empleado")
            self.root.geometry("1500x720")
            self.root.config(bg="#FFF7EC")

            Menu.cargar_menu()
            Inventario.cargar_stock()

            self.productos = Menu.obtener_todos_productos()
            self.carrito = []
            self.empleado = Empleado("Empleado1", "Empcafe123")

            frame_productos_titulo = tk.Frame(self.root, bg="#FFF7EC")
            frame_productos_titulo.pack(pady=(10, 0))
            tk.Label(frame_productos_titulo, text="Productos", font=("Arial", 16, "bold"), bg="#FFF7EC").pack()
            self.frame_productos = tk.Frame(self.root, bg="#FFF7EC")
            self.frame_productos.pack(side="left", fill="both", expand=True, padx=(20, 10), pady=(0, 20))
            self.mostrar_productos(self.frame_productos)

            frame_carrito_titulo = tk.Frame(self.root, bg="#FFF7EC")
            frame_carrito_titulo.pack(pady=(10, 0))
            tk.Label(frame_carrito_titulo, text="Carrito de Compras", font=("Arial", 16, "bold"), bg="#FFF7EC").pack()
            self.frame_carrito = tk.Frame(self.root, bg="#FFF7EC")
            self.frame_carrito.pack(side="right", fill="both", expand=True, padx=(10, 20), pady=(0, 20))
            self.mostrar_carrito(self.frame_carrito)

            self.frame_resumen = tk.Frame(self.root, bg="#EFE1D1")
            self.frame_resumen.pack(side="bottom", fill="x", padx=20, pady=(10, 20))
            self.mostrar_resumen(self.frame_resumen)
        except Exception as e:
            messagebox.showerror("Error en Ventemple.__init__", f"Error: {e}\n{traceback.format_exc()}")

    def mostrar_productos(self, frame):
        try:
            columnas = 6
            fila = 0
            columna = 0
            for producto in self.productos:
                self.frame_producto = tk.Frame(frame, relief="solid", borderwidth=1, padx=5, pady=5, bg="white")
                self.frame_producto.grid(row=fila, column=columna, padx=5, pady=5)

                label_nombre = tk.Label(
                    self.frame_producto, text=producto.nombre, font=("Arial", 10, "bold"), bg="white")
                label_nombre.pack()
                label_precio = tk.Label(
                    self.frame_producto, text=f"${producto.precio:.2f}", bg="white")
                label_precio.pack()
                btn_agregar = tk.Button(
                    self.frame_producto, text="Agregar",
                    command=lambda p=producto: self.agregar_producto(p), bg="#A67B5B", fg="white")
                btn_agregar.pack(pady=5)

                columna += 1
                if columna == columnas:
                    columna = 0
                    fila += 1
        except Exception as e:
            messagebox.showerror("Error", f"Error en mostrar_productos: {e}\n{traceback.format_exc()}")

    def agregar_producto(self, producto):
            self.carrito.append({"producto": producto, "cantidad": 1, "opciones": {}})
            self.mostrar_carrito(self.frame_carrito)
            self.mostrar_resumen(self.frame_resumen)

    def modificar_cantidad(self, index, cambio):
            self.carrito[index]["cantidad"] += cambio
            if self.carrito[index]["cantidad"] < 1:
                del self.frame_carrito[index]
            self.mostrar_carrito(self.frame_carrito)
            self.mostrar_resumen(self.frame_resumen)

    def mostrar_carrito(self, frame):
        try:
            for widget in frame.winfo_children():
                widget.destroy()

            if not self.carrito:
                tk.Label(frame, text="El carrito está vacío",
                         font=("Arial", 12), bg="#FFF7EC").pack()
                return

            for i, item in enumerate(self.carrito):
                frame_item = tk.Frame(frame, pady=2, bg="#FFF7EC")
                frame_item.pack(fill="x")

                label_nombre = tk.Label(
                    frame_item, text=item["producto"].nombre, width=20, anchor="w", bg="#FFF7EC")
                label_nombre.pack(side="left")

                btn_restar = tk.Button(
                    frame_item, text="-", width=3,
                    command=lambda idx=i: self.modificar_cantidad(idx, -1), bg="#A67B5B", fg="white")
                btn_restar.pack(side="left")

                label_cantidad = tk.Label(
                    frame_item, text=f" {item['cantidad']} ", width=3, bg="white")
                label_cantidad.pack(side="left")

                btn_sumar = tk.Button(
                    frame_item, text="+", width=3,
                    command=lambda idx=i: self.modificar_cantidad(idx, 1), bg="#A67B5B", fg="white")
                btn_sumar.pack(side="left")

                label_precio = tk.Label(
                    frame_item, text=f"${item['producto'].precio * item['cantidad']:.2f}", width=8,
                    anchor="e", bg="#FFF7EC")
                label_precio.pack(side="right")
        except Exception as e:
            messagebox.showerror("Error", f"Error en mostrar_carrito: {e}\n{traceback.format_exc()}")

    def mostrar_resumen(self, frame):
        try:
            for widget in frame.winfo_children():
                widget.destroy()

            subtotal = sum(item["producto"].precio *
                           item["cantidad"] for item in self.carrito)
            impuesto = (subtotal) * 0.015  
            total = subtotal + impuesto

            tk.Label(frame, text=f"Subtotal: ${subtotal:.2f}",
                     anchor="e", bg="#EFE1D1").pack(fill="x")
            tk.Label(frame, text=f"Impuesto (1.5%): ${impuesto:.2f}",
                     anchor="e", bg="#EFE1D1").pack(fill="x")
            tk.Label(frame, text=f"Total: ${total:.2f}",
                     font=("Arial", 12, "bold"), anchor="e", bg="#EFE1D1").pack(fill="x")

            frame_botones = tk.Frame(frame, bg="#EFE1D1")
            frame_botones.pack(pady=10)

            btn_cancelar = tk.Button(
                frame_botones, text="Cancelar Orden", command=self.cancelar_pedido, bg="#FF5733",
                fg="white", width=15)
            btn_cancelar.pack(side="left", padx=5)

            btn_pagar = tk.Button(
                frame_botones, text=f"Pagar (${total:.2f})", command=self.pagar_pedido, bg="#4CAF50",
                fg="white", width=15)
            btn_pagar.pack(side="left", padx=5)
        except Exception as e:
            messagebox.showerror("Error", f"Error en mostrar_resumen: {e}\n{traceback.format_exc()}")

    def cancelar_pedido(self):
        try:
            self.carrito.clear()
            self.mostrar_carrito(self.frame_carrito)
            self.mostrar_resumen(self.frame_resumen)
        except Exception as e:
            messagebox.showerror("Error", f"Error en cancelar_pedido: {e}\n{traceback.format_exc()}")

    def pagar_pedido(self):
        try:
            if not self.carrito:
                messagebox.showinfo("Aviso", "No hay productos en el pedido.")
                return

            pedido = self.empleado.crear_pedido(
                "Cliente", [{"producto": item["producto"], "opciones": item["opciones"]} for item in self.carrito])
            if pedido:
                messagebox.showinfo(
                    "Pedido exitoso", f"Pedido #{pedido.id} guardado\nTotal: ${pedido.total():.2f}")
                self.carrito.clear()
                self.mostrar_carrito(self.frame_carrito)
                self.mostrar_resumen(self.frame_resumen)
        except Exception as e:
            messagebox.showerror("Error", f"Error en pagar_pedido: {e}\n{traceback.format_exc()}")

    def mostrar_ticket(self, pedido):
        ticket_window = Toplevel(self.root)
        ticket_window.title(f"Ticket Pedido #{pedido.id}")
        frame_ticket = tk.Frame(ticket_window)
        Scrollbar_ticket = Scrollbar(frame_ticket)
        text_ticket = Text(frame_ticket, width=40, height=20) 
        Scrollbar_ticket.pack(side="right", fill="y")
        text_ticket.pack(side="left", fill="both", expand=True)
        text_ticket.config(yscrollcommand=Scrollbar_ticket.set)
        Scrollbar_ticket.config(command=text_ticket.yview)
        frame_ticket.pack(fill="both", expand=True)

        text_ticket.insert(tk.END, "==== CAFETERIA ====\n")
        text_ticket.insert(tk.END, f"Pedido #{pedido.id}\n")
        text_ticket.insert(tk.END, f"Cliente: {pedido.cliente}\n")
        text_ticket.insert(tk.END, "--------------------\n")

        for item in pedido.productos:
            text_ticket.insert(tk.END, f"{item['producto'].nombre} - $ {item['producto'].precio:.2f}\n")
            if item['opciones']:
                text_ticket.insert(tk.END, f"Opciones: {', '.join(item['opciones'])}\n")
                text_ticket.insert(tk.END, "--------------------\n")
                text_ticket.insert(tk.END, f"Total: ${pedido.total():.2f}\n")
                text_ticket.insert(tk.END, "¡Gracias por su compra!\n")
                text_ticket.config(state="disabled")

    def finalizar_pedido(self):
        if not self.carrito:
            messagebox.showinfo("No hay productos en el pedido.")
        return
        pedido = self.empleado.crear_pedido("Cliente", [ {"producto": item["producto"], "opciones": item["opciones"] } for item in self.carrito ])
        if pedido:
            messagebox.showinfo("Pedido exitoso", f"Pedido #{pedido.id} guardado\nTotal: ${pedido.total():.2f}")
            self.mostrar_ticket(pedido)  
            self.carrito.clear()
            self.mostrar_carrito()

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaInicio(root)
    root.mainloop()