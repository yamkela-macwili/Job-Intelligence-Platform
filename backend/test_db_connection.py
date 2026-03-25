#!/usr/bin/env python3
"""Test database connection."""
import sys
import os

# Test without external dependencies first
print("Testing PostgreSQL connection...")
print("=" * 60)

try:
    import psycopg2
    print("✓ psycopg2 is installed")
    
    # Try to connect
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="job_intelligence",
            user="user",
            password=os.getenv("DB_PASSWORD", "password")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✓ Connected to PostgreSQL: {version[0][:50]}...")
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cvs (
                id UUID PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                raw_text TEXT NOT NULL,
                processed_text TEXT,
                skills_extracted TEXT DEFAULT '[]',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id UUID PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                skills_required TEXT DEFAULT '[]',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id UUID PRIMARY KEY,
                cv_id UUID NOT NULL REFERENCES cvs(id),
                job_id UUID REFERENCES jobs(id),
                match_score INTEGER DEFAULT 0,
                missing_skills TEXT DEFAULT '[]',
                strengths TEXT DEFAULT '[]',
                recommendations TEXT,
                roadmap TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
        print("✓ Tables created successfully")
        
        cursor.close()
        conn.close()
        print("\n✓ Database setup complete!")
        sys.exit(0)
        
    except psycopg2.OperationalError as e:
        print(f"✗ Connection failed: {e}")
        print("\nTry running:")
        print("  psql -h localhost -U user -d job_intelligence")
        print("\nOr set password in environment:")
        print("  export DB_PASSWORD='your_password'")
        sys.exit(1)
        
except ImportError:
    print("✗ psycopg2 not installed")
    print("Install it with: pip install psycopg2-binary")
    sys.exit(1)
