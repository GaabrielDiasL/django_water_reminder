# Usar uma imagem base oficial do Python
FROM python:3.9-slim

# Configurar variáveis de ambiente
ENV PYTHONUNBUFFERED 1

# Criar e definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt /app/

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o conteúdo do projeto para o diretório de trabalho no container
COPY . /app/

# Expôr a porta que o Django usa
EXPOSE 8000


# Comando padrão para iniciar o servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
