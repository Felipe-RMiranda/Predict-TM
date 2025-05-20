from rest_framework.response import Response
import numpy as np
from rest_framework.decorators import api_view
from rest_framework import status
import os
import cv2
from tensorflow.keras.models import load_model
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import base64
import imghdr
from django.contrib.staticfiles.storage import staticfiles_storage

# Caminho para o modelo
modelPath = os.path.join('diagnostics', 'cnn_tumor_model.h5')
# Carrega o modelo treinado
if not os.path.exists(modelPath):
    raise FileNotFoundError(f"❌ Modelo não encontrado em: {modelPath}")
model = load_model(modelPath)
print("✅ Modelo carregado com sucesso.")

def imgProcessing(img_bytes):
    """Lê uma imagem, converte para escala de cinza, redimensiona para 128x128
    e normaliza os pixels entre 0 e 1."""

    # Ler os bytes da imagem
    imgBytes = np.asarray(bytearray(img_bytes), dtype=np.uint8)

    # Decodificar com OpenCV como imagem em escala de cinza
    imagem = cv2.imdecode(imgBytes, cv2.IMREAD_GRAYSCALE)
    if imagem is None:
        raise ValueError("❌ Erro ao carregar imagem!")

    imagem = cv2.resize(imagem, (128, 128))
    imagem = imagem.astype('float32') / 255.0
    imagem = imagem.reshape(1, 128, 128, 1)
    return imagem

def imgPredict(img, img_bytes):
    """Realiza a previsão de uma única imagem."""
    print(f"🔎 Analisando imagem: {img}")
    prob = model.predict(imgProcessing(img_bytes))[0][0]

    resumo = " • Possível presença de tumor (TM). Recomenda-se a apresentação deste documento ao especialista responsável."
    

    if prob >= 0.5:
        statusC = "Possível TM detectado"
        resumo = " • Possível presença de tumor (TM). Recomenda-se a apresentação deste documento ao especialista responsável."
        print(resumo)
        print("🚨 Indício de tumor detectado!")
    else:
        statusC = "Cerebro saudável."
        resumo = " • Não foi encontrado alterações relevantes."
        print(resumo)
        print("✅ Cérebro saudável detectado.")

    return prob, resumo, statusC

@api_view(['POST'])
def getDiagnosis(request):
    if request.method == 'GET':
        print("🔍 Requisição GET recebida em /api/getDiagnosis/")
        print("🌐 Origem:", request.META.get('HTTP_REFERER'))
        print("🧠 User-Agent:", request.META.get('HTTP_USER_AGENT'))
        print("📍 Endereço IP:", request.META.get('REMOTE_ADDR'))
        return JsonResponse({'erro': 'Use POST para enviar a imagem.'}, status=405)

    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        img = request.FILES.get('img')  # <- Nome da chave usada no FormData

    if not all([name, age, gender, img]):
        return JsonResponse({'erro': 'Dados incompletos.'}, status=400)

    img_bytes = img.read()
    # Detecta o tipo da imagem
    img_type = imghdr.what(None, h=img_bytes)
    # Define o MIME type correspondente
    mime_type = f"image/{img_type}" if img_type else "image/jpeg"  # Fallback em caso de erro
    # Monta o base64 com prefixo correto
    img64 = f"data:{mime_type};base64,{base64.b64encode(img_bytes).decode('utf-8')}"
    prob, result, statusC = imgPredict(img, img_bytes)
    context = {
        'name': name,
        'age': age,
        'gender': gender,
        'img': img64,  # ou use o sistema de media do Django
        'probability': prob,
        'status': statusC,
        'result': result
    }
    print(f"\n🧠 Resultado da análise: {result}")
    return render(request, 'deshboard.html', context)

def upForm(request):
    return render(request, 'upform.html')

def deshboard(request):
    context = {
        'name': 'João Torres',
        'age': '37',
        'gender': 'Masculino',
        'img': staticfiles_storage.url('test4.jpg'),
        'probability': '0.42077708',
        'status': 'Cerebro saudável.',
        'result': '• Não foi encontrado alterações relevantes.'
    }
    return render(request, 'deshboard.html', context)
