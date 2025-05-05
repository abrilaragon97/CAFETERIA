import json
import os

MENU_JSON = "menu.json"
PEDIDOS_JSON = "pedidos.json"
USUARIOS_JSON = "usuarios.json"
INVENTARIO_JSON = "inventario.json" 

class Usuario:
    lista_usuarios = []

    def __init__(self, nombre, rol, password):
        self.nombre = nombre
        self.rol = rol
        self.__password = password
        Usuario.lista_usuarios.append(self)

    def validar_password(self, password):
        return self.__password == password

    @classmethod
    def iniciar_sesion(cls, nombre, password):
        for usuario in cls.lista_usuarios:
            if usuario.nombre == nombre and usuario.validar_password(password):
                print(f"Sesión iniciada como {usuario.rol}")
                return usuario
        print("Datos incorrectos.")
        return None

    @classmethod
    def cargar_usuarios(cls):
        cls.lista_usuarios.clear()
        if os.path.exists(USUARIOS_JSON):
            with open(USUARIOS_JSON, "r") as file:
                data = json.load(file)
                for u in data:
                    if u["rol"] == "Gerente":
                        Gerente (u["nombre"], u["password"])
                    elif u["rol"] == "Administrador":
                        Administrador (u["nombre"], u["password"])
                    elif u["rol"] == "Empleado":
                        Empleado (u["nombre"], u["password"])

    @classmethod
    def guardar_usuarios(cls):
        data = [{"nombre": u.nombre, "rol": u.rol, "password": u._Usuario__password} for u in cls.lista_usuarios]
        with open(USUARIOS_JSON, "w") as file:
            json.dump(data, file, indent=4)

class Gerente(Usuario):
    def __init__(self, nombre, password):
        super().__init__(nombre, "Gerente", password)

    def agregar_usuario(self, nombre, rol, password):
        if rol == "Administrador":
            Administrador(nombre, password)
        elif rol == "Empleado":
            Empleado(nombre, password)
        elif rol == "Gerente":
            Gerente(nombre, password)
        Usuario.guardar_usuarios()
        print(f"Usuario {nombre} agregado como {rol}.")

    def eliminar_usuario(self, nombre):
        for u in Usuario.lista_usuarios:
            if u.nombre == nombre:
                Usuario.lista_usuarios.remove(u)
                Usuario.guardar_usuarios()
                print(f"Usuario {nombre} eliminado.")
                return
        print("Usuario no registrado.")

    def ver_pedidos(self):
        for p in Pedido.lista_pedidos:
            print(f"Pedido #{p.id} - Cliente: {p.cliente} - Total: ${p.total():.2f}")

    def modificar_stock(self, ingrediente, cantidad):
        Inventario.stock[ingrediente] = cantidad
        Inventario.guardar_stock()
        print(f"Stock actualizado: {ingrediente} = {cantidad}")

class Administrador(Usuario):
    def __init__(self, nombre, password):
        super().__init__(nombre, "Administrador", password)

    def agregar_producto(self, seccion, categoria, producto_dict):
        Menu.categorias[seccion][categoria].append(producto_dict)
        self.guardar_menu()
        print(f"Producto '{producto_dict['nombre']}' agregado a {seccion} > {categoria}")

    def guardar_menu(self):
        with open(MENU_JSON, "w", encoding="utf-8") as file:
            json.dump({"menu": Menu.categorias}, file, indent=4, ensure_ascii=False)

    def actualizar_stock(self, ingrediente, cantidad):
        Inventario.stock[ingrediente] = cantidad
        Inventario.guardar_stock()
        print(f"Stock actualizado: {ingrediente} = {cantidad}")

class Empleado(Usuario):
    def __init__(self, nombre, password):
        super().__init__(nombre, "Empleado", password)

    def crear_pedido(self, cliente, lista_productos):
        nuevo_id = len(Pedido.lista_pedidos) + 1
        print("INICIO DE PEDIDO")
        print(f"Cliente: {cliente}")
        print(f"Lista de productos: {lista_productos}")
        for item in lista_productos:
            producto = item["producto"] 
            print(f"Producto: {producto.nombre}, Ingrdientes: {producto.ingredientes}")
            for ingrediente in producto.ingredientes:
                print("Verificando ingredientes: '{ingrdiente}'")
                disponible, faltante = Inventario.verificar_ingredientes(producto.ingredientes)
                if not disponible:
                    print(f"No se puede procesar el pedido, falta: {faltante}")
                    return None
            
            for item in lista_productos:
                producto = item["producto"]  
                Inventario.usar_ingredientes(producto.ingredientes)  
                nuevo_pedido = Pedido(nuevo_id, cliente, lista_productos)
                Pedido.guardar_pedidos()
                print(f"Pedido #{nuevo_id} creado correctamente.")
                print("FIN DE PEDIDO")
                return nuevo_pedido

class Producto:
    def __init__(self, id, nombre, precio, ingredientes, opciones=None):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.ingredientes = ingredientes
        self.opciones = opciones or []

class Inventario:
    stock = {}

    @classmethod
    def cargar_stock(cls):
        if os.path.exists(INVENTARIO_JSON):
            with open(INVENTARIO_JSON, "r", encoding="utf-8") as file:
                cls.stock = json.load(file)

    @classmethod
    def guardar_stock(cls):
        with open(INVENTARIO_JSON, "w", encoding="utf-8") as file:
            json.dump(cls.stock, file, indent=4, ensure_ascii=False)

    @staticmethod
    def verificar_ingredientes(ingredientes):
        faltante = []
        disponible = True
        print(f"Verificando lista de ingredientes: {ingredientes}, Tipo: {type(ingredientes)}")
        if not isinstance(ingredientes, list):
            print("ERROR: Ingredientes no es una lista!")
            return False, ["ERROR"]
        if not ingredientes:  
            print("Lista de ingredientes vacía: No hay ingredientes que verificar.")
            return True, [] 
        for ingrediente in ingredientes:
            print(f"Verificando ingrediente individual: '{ingrediente}', Tipo: {type(ingrediente)}")
            if not isinstance(ingrediente, str):
                print(f"    ERROR: '{ingrediente}' no es una cadena")
                faltante.append(str(ingrediente))  
                disponible = False
            if ingrediente not in Inventario.stock:
                print(f"    '{ingrediente}' no disponible en inventario")
                faltante.append(ingrediente)
                disponible = False
            elif Inventario.stock[ingrediente] == 0:  
                print(f"    '{ingrediente}' tiene cero en stock")
                faltante.append(ingrediente)
                disponible = False
        return disponible, faltante

    @classmethod
    def usar_ingredientes(cls, ingredientes):
        disponible, falta = cls.verificar_ingredientes(ingredientes)
        if not disponible:
            print(f"Ingrediente agotado: {falta}")
            return False
        for ing in ingredientes:
            cls.stock[ing] -= 1
        cls.guardar_stock()
        return True

class Menu:
    categorias = {}

    @classmethod
    def cargar_menu(cls):
        if os.path.exists(MENU_JSON):
            with open(MENU_JSON, "r", encoding="utf-8") as file:
                data = json.load(file)
                cls.categorias = data["menu"]

    @classmethod
    def obtener_todos_productos(cls):
        productos = []
        for grupo in cls.categorias.values():
            if isinstance(grupo, dict):
                for categoria in grupo.values():
                    for item in categoria:
                        productos.append(Producto(**item))
            elif isinstance(grupo, list):
                for item in grupo:
                    productos.append(Producto(**item))
        return productos

class Pedido:
    lista_pedidos = []

    def __init__(self, id_pedido, cliente, productos):
        self.id = id_pedido
        self.cliente = cliente
        self.productos = productos 
        Pedido.lista_pedidos.append(self)

    def total(self):
        return sum(p["producto"].precio for p in self.productos)

    @classmethod
    def guardar_pedidos(cls):
        data = []
        for pedido in cls.lista_pedidos:
            data.append({
                "id": pedido.id,
                "cliente": pedido.cliente,
                "productos": [{
                    "id": p["producto"].id,
                    "nombre": p["producto"].nombre,
                    "precio": p["producto"].precio,
                    "opciones": p["opciones"]
                } for p in pedido.productos],
                "total": pedido.total()
            })
        with open(PEDIDOS_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
