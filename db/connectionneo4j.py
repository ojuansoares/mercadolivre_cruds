from neo4j import GraphDatabase

URI = "neo4j+s://addb0709.databases.neo4j.io"
AUTH = ("neo4j", "iYiSjX7P9tcFzaxzAlJyMspDS6DOrwW9l7-ae-bcevk")

def get_session():
    try:
        driver = GraphDatabase.driver(URI, auth=AUTH)
        session = driver.session()
        return session
    except Exception as e:
        print(f"Failed to get session: {e}")
        return None

def get_verification():
    try:
        driver = GraphDatabase.driver(URI, auth=AUTH)
        verify = driver.verify_connectivity()
        return verify
    except Exception as e:
        print("Failed to get verification")

def check_neo4j_connection():
    try:
        get_verification()
        print("Neo4j connection is OK")
    except Exception as e:
        print(f"Failed to connect to Neo4j: {e}")