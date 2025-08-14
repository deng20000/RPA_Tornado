#!/usr/bin/env python3
import psycopg2
import sys
import traceback

def test_basic_connection(host, port, database, username, password):
    try:
        print(f"Attempting connection to {host}:{port}...")
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password,
            connect_timeout=5
        )
        print("Connection established successfully!")
        
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()[0]
        
        print(f"SUCCESS: Basic connection works")
        print(f"Test query result: {result}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"DETAILED ERROR:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print(f"Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Detailed PostgreSQL Connection Test")
    print("=" * 40)
    
    # Test with minimal connection first
    print("\nTesting dbadmin user with detailed error info:")
    success = test_basic_connection("127.0.0.1", 5432, "rpa_tornado", "dbadmin", "admin123")
    
    if not success:
        print("\n" + "="*50)
        print("DIAGNOSIS:")
        print("The error suggests a character encoding issue.")
        print("This might be related to:")
        print("1. PostgreSQL server locale settings")
        print("2. psycopg2 library version compatibility")
        print("3. Windows system locale settings")
        print("\nLet's try pgAdmin4 directly with these settings:")
        print("- Host: 127.0.0.1")
        print("- Port: 5432")
        print("- Username: dbadmin")
        print("- Password: admin123")
        print("- Database: rpa_tornado")
        print("- SSL Mode: Disable")