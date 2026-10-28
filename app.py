import math
from datetime import date
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__, template_folder="plantillas")

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hotel_reservas",
        port=3306
    )


@app.route("/", methods=["GET"])
def inicio():
    resultados = []
    error = None

    ciudad = request.args.get("ciudad", "")
    personas = request.args.get("personas", "2")
    tipo = request.args.get("tipo", "")
    temporada = request.args.get("temporada", "baja")
    fecha_entrada = request.args.get("entrada", "")
    fecha_salida = request.args.get("salida", "")

    if request.args.get("buscar"):
        conexion = None
        cursor = None

        try:
            cantidad_personas = int(personas)

            if cantidad_personas < 1:
                raise ValueError("Pon al menos una persona.")

            if not fecha_entrada or not fecha_salida:
                raise ValueError("Elige las fechas de entrada y salida.")

            entrada = date.fromisoformat(fecha_entrada)
            salida = date.fromisoformat(fecha_salida)

            if salida <= entrada:
                raise ValueError("La salida tiene que ser despues de la entrada.")

            noches = (salida - entrada).days

            conexion = conectar()
            cursor = conexion.cursor(dictionary=True)

            consulta = """
                SELECT h.nombre, h.ciudad, hab.id AS habitacion_id,
                       hab.tipo, hab.capacidad, hab.cantidad, t.precio
                FROM hoteles h
                JOIN habitaciones hab ON hab.hotel_id = h.id
                JOIN tarifas t ON t.habitacion_id = hab.id
                WHERE t.temporada = %s
            """
            valores = [temporada]

            if ciudad:
                consulta += " AND h.ciudad = %s"
                valores.append(ciudad)

            if tipo:
                consulta += " AND hab.tipo = %s"
                valores.append(tipo)

            cursor.execute(consulta, valores)
            habitaciones = cursor.fetchall()

            for habitacion in habitaciones:
                capacidad = habitacion["capacidad"]
                cantidad = habitacion["cantidad"]

                if capacidad <= 0 or cantidad <= 0:
                    continue

                cuartos_necesarios = math.ceil(cantidad_personas / capacidad)

                cursor.execute("""
                    SELECT COALESCE(SUM(cantidad_habitaciones), 0) AS ocupadas
                    FROM reservas
                    WHERE habitacion_id = %s
                    AND estado = 'confirmada'
                    AND fecha_entrada < %s
                    AND fecha_salida > %s
                """, (habitacion["habitacion_id"], salida, entrada))

                reserva = cursor.fetchone()
                ocupadas = int(reserva["ocupadas"])
                disponibles = cantidad - ocupadas

                if disponibles >= cuartos_necesarios:
                    habitacion["cuartos_necesarios"] = cuartos_necesarios
                    habitacion["disponibles"] = disponibles
                    habitacion["noches"] = noches
                    habitacion["total"] = (
                        float(habitacion["precio"])
                        * cuartos_necesarios
                        * noches
                    )
                    resultados.append(habitacion)

        except (ValueError, TypeError) as e:
            error = str(e)

        except mysql.connector.Error:
            error = "No pude consultar la base de datos. Revisa MySQL y las tablas."

        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

    return render_template(
        "inicio.html",
        resultados=resultados,
        error=error,
        ciudad=ciudad,
        personas=personas,
        tipo=tipo,
        temporada=temporada,
        entrada=fecha_entrada,
        salida=fecha_salida
    )


if __name__ == "__main__":
    app.run(debug=True)
