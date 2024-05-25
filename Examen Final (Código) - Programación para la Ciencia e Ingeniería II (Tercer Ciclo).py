# Examen Final (Código)
# Nombre Completo: Paulo Andrés Galán Cortés
# Carnet: 5212-23-10107

# //////////////////////////////////////////////////////////////////////////////////

import json
from flet import Page, Text, TextField, ElevatedButton, Row, Column, Dropdown, DropdownItem, IconButton, icons

# Archivos JSON para almacenar datos
PERSONAS_FILE = "personas.json"
HORAS_EXTRAS_FILE = "horas_extras.json"

# Cargar datos de JSON
def cargar_datos(archivo):
    try:
        with open(archivo, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Guardar datos en JSON
def guardar_datos(archivo, datos):
    with open(archivo, "w") as file:
        json.dump(datos, file, indent=4)

# Función para crear la pantalla de ingreso de personas
def crear_pantalla_ingreso_personas(page):
    nombre_input = TextField(label="Nombre")
    codigo_input = TextField(label="Código")
    costo_hora_extra_input = TextField(label="Costo por Hora Extra", keyboard_type="number")
    mensaje = Text()
    
    def guardar_persona(e):
        personas = cargar_datos(PERSONAS_FILE)
        codigo = codigo_input.value
        personas[codigo] = {
            "nombre": nombre_input.value,
            "costo_hora_extra": float(costo_hora_extra_input.value)
        }
        guardar_datos(PERSONAS_FILE, personas)
        mensaje.value = "Persona guardada exitosamente"
        mensaje.update()
    
    return Column([
        Text("Ingreso de Personas"),
        nombre_input,
        codigo_input,
        costo_hora_extra_input,
        ElevatedButton(text="Guardar", on_click=guardar_persona),
        mensaje
    ])

# Función para crear la pantalla de ingreso de horas extras
def crear_pantalla_ingreso_horas_extras(page):
    codigo_input = TextField(label="Código")
    horas_extras_input = TextField(label="Horas Extras", keyboard_type="number")
    mensaje = Text()
    
    def guardar_horas_extras(e):
        horas_extras = cargar_datos(HORAS_EXTRAS_FILE)
        codigo = codigo_input.value
        horas_extras[codigo] = {
            "horas_extras": float(horas_extras_input.value)
        }
        guardar_datos(HORAS_EXTRAS_FILE, horas_extras)
        mensaje.value = "Horas extras guardadas exitosamente"
        mensaje.update()
    
    return Column([
        Text("Ingreso de Horas Extras"),
        codigo_input,
        horas_extras_input,
        ElevatedButton(text="Guardar", on_click=guardar_horas_extras),
        mensaje
    ])

# Función para crear la pantalla de reporte de horas extras y pago
def crear_pantalla_reporte(page):
    codigo_input = TextField(label="Código")
    mensaje = Text()
    
    def generar_reporte(e):
        personas = cargar_datos(PERSONAS_FILE)
        horas_extras = cargar_datos(HORAS_EXTRAS_FILE)
        codigo = codigo_input.value
        
        if codigo in personas and codigo in horas_extras:
            nombre = personas[codigo]["nombre"]
            costo_hora_extra = personas[codigo]["costo_hora_extra"]
            horas = horas_extras[codigo]["horas_extras"]
            total_pagar = costo_hora_extra * horas
            mensaje.value = f"Nombre: {nombre}\nHoras Extras: {horas}\nTotal a Pagar: ${total_pagar:.2f}"
        else:
            mensaje.value = "Código no encontrado"
        mensaje.update()
    
    return Column([
        Text("Reporte de Horas Extras y Pago"),
        codigo_input,
        ElevatedButton(text="Generar Reporte", on_click=generar_reporte),
        mensaje
    ])

# Función principal
def main(page: Page):
    page.title = "Sistema de Control de Horas Extras"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def navegar_a(e, pantalla):
        page.views.clear()
        page.views.append(pantalla)
        page.update()
    
    ingreso_personas_button = ElevatedButton(
        text="Ingreso de Personas", 
        on_click=lambda e: navegar_a(e, crear_pantalla_ingreso_personas(page))
    )
    ingreso_horas_extras_button = ElevatedButton(
        text="Ingreso de Horas Extras", 
        on_click=lambda e: navegar_a(e, crear_pantalla_ingreso_horas_extras(page))
    )
    reporte_button = ElevatedButton(
        text="Reporte de Horas Extras y Pago", 
        on_click=lambda e: navegar_a(e, crear_pantalla_reporte(page))
    )
    
    page.add(Column([
        Text("Sistema de Control de Horas Extras", size=30, weight="bold"),
        ingreso_personas_button,
        ingreso_horas_extras_button,
        reporte_button
    ]))

if __name__ == "__main__":
    from flet import app
    app(target=main)
