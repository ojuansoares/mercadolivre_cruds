import redis
import os
from dotenv import load_dotenv

# Carregar as variáveis do .env
load_dotenv()

rediscon = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT')),
    password=os.getenv('REDIS_PASSWORD')
)

def check_redis_connection():
    try:
        rediscon.ping()
        print("Conectado ao Redis!")
    except redis.ConnectionError:
        print("Erro ao conectar ao Redis.")
