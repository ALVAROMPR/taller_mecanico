"""
ai_services.py
Servicio de IA para el Taller Mecánico.
Usa OpenRouter API con modelo DeepSeek.

La API key se lee desde config.py (variable de entorno).
NUNCA hardcodear la key directamente en este archivo.
"""

import requests
import json
from flask import current_app


# ══════════════════════════════════════════════
# CLIENTE BASE
# ══════════════════════════════════════════════

def _llamar_ia(prompt: str, max_tokens: int = 800) -> str:
    """
    Función base que llama a OpenRouter/DeepSeek.
    Retorna el texto de respuesta o un mensaje de error legible.
    No lanza excepciones — siempre retorna string.
    """
    api_key = current_app.config.get("OPENROUTER_API_KEY", "")
    model   = current_app.config.get("OPENROUTER_MODEL", "deepseek/deepseek-chat-v3-0324")
    base_url = current_app.config.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

    if not api_key:
        return "⚠️ API key no configurada. Agrega OPENROUTER_API_KEY en config.py o como variable de entorno."

    try:
        response = requests.post(
            url=f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000",   # requerido por OpenRouter
                "X-Title": "Taller Mecánico"
            },
            data=json.dumps({
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Eres un asistente experto en gestión de talleres mecánicos. "
                            "Respondes siempre en español, de forma clara, concisa y profesional. "
                            "Tus análisis deben ser prácticos y orientados a la toma de decisiones del taller."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.4
            }),
            timeout=30        # DeepSeek puede tardar hasta 25 s en respuestas largas
        )

        if response.status_code != 200:
            return f"⚠️ Error de API ({response.status_code}): {response.text[:200]}"

        resultado = response.json()
        return resultado["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        return "⚠️ La IA tardó demasiado en responder. Intenta de nuevo en unos segundos."
    except requests.exceptions.ConnectionError:
        return "⚠️ No se pudo conectar con el servicio de IA. Verifica tu conexión a internet."
    except (KeyError, IndexError, ValueError) as e:
        return f"⚠️ Respuesta inesperada de la API: {e}"
    except Exception as e:
        return f"⚠️ Error inesperado: {e}"


# ══════════════════════════════════════════════
# FUNCIÓN 1 — Análisis general del taller
# ══════════════════════════════════════════════

def analizar_taller(
    ingresos_totales: float,
    total_ordenes: int,
    ordenes_pendientes: int,
    ordenes_en_proceso: int,
    ordenes_finalizadas: int,
    ordenes_entregadas: int,
    servicios_populares: list   # lista de tuplas (nombre, cantidad)
) -> str:
    """
    Recibe los KPIs del dashboard y pide a la IA un resumen
    ejecutivo con conclusiones y recomendaciones.
    """
    servicios_str = "\n".join(
        f"  - {nombre}: {cantidad} usos"
        for nombre, cantidad in servicios_populares
    ) or "  (sin datos de servicios aún)"

    prompt = f"""
Analiza los siguientes datos operativos de un taller mecánico y genera:
1. Un resumen ejecutivo en 2-3 oraciones.
2. Los 2 puntos más destacados (positivos o negativos).
3. Dos recomendaciones concretas y accionables para el taller.

DATOS DEL TALLER:
- Ingresos totales: Bs {ingresos_totales:.2f}
- Total de órdenes: {total_ordenes}
- Órdenes pendientes: {ordenes_pendientes}
- Órdenes en proceso: {ordenes_en_proceso}
- Órdenes finalizadas: {ordenes_finalizadas}
- Órdenes entregadas: {ordenes_entregadas}

SERVICIOS MÁS SOLICITADOS:
{servicios_str}

Responde en formato claro con secciones: Resumen, Puntos Destacados, Recomendaciones.
""".strip()

    return _llamar_ia(prompt, max_tokens=600)


# ══════════════════════════════════════════════
# FUNCIÓN 2 — Análisis de servicios populares
# ══════════════════════════════════════════════

def analizar_servicios(servicios_populares: list) -> str:
    """
    Recibe lista de (nombre_servicio, cantidad_usos) y pide
    análisis de tendencias y recomendaciones de catálogo.
    """
    if not servicios_populares:
        return "No hay datos de servicios suficientes para analizar."

    servicios_str = "\n".join(
        f"  {i+1}. {nombre}: {cantidad} veces solicitado"
        for i, (nombre, cantidad) in enumerate(servicios_populares)
    )

    prompt = f"""
Analiza el siguiente ranking de servicios de un taller mecánico:

{servicios_str}

Proporciona:
1. Qué servicios son los más rentables o frecuentes y por qué.
2. Si hay servicios que probablemente se deberían promocionar más.
3. Una sugerencia de nuevo servicio que complemente bien el catálogo actual.

Sé breve y directo, máximo 150 palabras.
""".strip()

    return _llamar_ia(prompt, max_tokens=400)


# ══════════════════════════════════════════════
# FUNCIÓN 3 — Recomendación de mantenimiento
# ══════════════════════════════════════════════

def recomendar_mantenimiento(
    marca: str,
    modelo: str,
    anio: int,
    servicios_previos: list   # lista de strings con nombres de servicios ya realizados
) -> str:
    """
    Dado un vehículo y su historial de servicios,
    recomienda los próximos mantenimientos preventivos.
    """
    historial_str = (
        "\n".join(f"  - {s}" for s in servicios_previos)
        if servicios_previos
        else "  (sin historial de servicios previos)"
    )

    prompt = f"""
Eres un mecánico experto. Dado el siguiente vehículo e historial de servicios,
recomienda los próximos 3 mantenimientos preventivos más importantes.

VEHÍCULO:
- Marca: {marca}
- Modelo: {modelo}
- Año: {anio}

SERVICIOS YA REALIZADOS EN EL TALLER:
{historial_str}

Para cada mantenimiento recomendado indica:
- Nombre del servicio
- Por qué es importante en este momento
- Urgencia: Alta / Media / Baja

Responde de forma concisa, máximo 200 palabras.
""".strip()

    return _llamar_ia(prompt, max_tokens=500)