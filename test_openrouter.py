#!/usr/bin/env python3
"""
Test de conexión con OpenRouter
"""

import os
import base64
import requests
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = "openrouter/free"

def create_test_image():
    """Crea una imagen de prueba simple con texto."""
    img = Image.new('RGB', (400, 200), color='white')
    return img

def image_to_base64(img: Image.Image) -> str:
    """Convierte una imagen PIL a base64."""
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def test_openrouter():
    """Prueba la conexión con OpenRouter."""
    
    if not OPENROUTER_API_KEY:
        print("❌ ERROR: OPENROUTER_API_KEY no está configurado en .env")
        return False
    
    print("🔑 API Key encontrada:", OPENROUTER_API_KEY[:20] + "...")
    print("🤖 Modelo:", OPENROUTER_MODEL)
    print("\n📡 Probando conexión con OpenRouter...\n")
    
    # Crear imagen de prueba
    test_img = create_test_image()
    image_b64 = image_to_base64(test_img)
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://quizsnap.local",
        "X-Title": "QuizSnap",
    }
    
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": "Describe brevemente esta imagen en una oración."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_b64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 100,
        "temperature": 0.1,
    }
    
    try:
        print("📤 Enviando solicitud...")
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📥 Status Code: {resp.status_code}")
        
        if resp.status_code != 200:
            print(f"❌ ERROR: {resp.status_code}")
            print(f"Respuesta: {resp.text}")
            return False
        
        data = resp.json()
        
        # Mostrar respuesta completa para debug
        print("\n📋 Respuesta JSON completa:")
        import json
        print(json.dumps(data, indent=2))
        
        choices = data.get("choices", [])
        if choices:
            content = choices[0]["message"]["content"]
            print(f"\n✅ ÉXITO! Respuesta recibida:")
            print(f"   {content}")
            return True
        else:
            print("❌ ERROR: No se encontraron 'choices' en la respuesta")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR de conexión: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR inesperado: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("  TEST DE CONEXIÓN - OPENROUTER")
    print("="*60 + "\n")
    
    success = test_openrouter()
    
    print("\n" + "="*60)
    if success:
        print("✅ TEST EXITOSO - OpenRouter está funcionando correctamente")
    else:
        print("❌ TEST FALLIDO - Revisa los errores arriba")
    print("="*60)
