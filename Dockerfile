# Use imagem oficial do Python
FROM python:3.11

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos para dentro do container
COPY . .

# Instala dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expõe a porta usada pelo Flask
EXPOSE 5000

# Comando para rodar o app
CMD ["python", "wsgi.py"]
