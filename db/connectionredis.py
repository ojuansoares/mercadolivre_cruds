import redis

rediscon = redis.Redis(
  host='redis-10558.c17.us-east-1-4.ec2.redns.redis-cloud.com',
  port=10558,
  password='MAa5PK8hWOv0D19ElVN25Rr6bok2axZJ')

def check_redis_connection():
    try:
        rediscon.ping()
        print("Conectado ao Redis!")
    except redis.ConnectionError:
        print("Erro ao conectar ao Redis.")