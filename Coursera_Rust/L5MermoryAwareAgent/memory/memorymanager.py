"""
Part 2: Memory Manager Initialization

The 'MemoryManager' class is the central abstraction that unifies
all memory operations. It provides a clean interface for reading 
and writing to different memory types, hiding the complexity of SQL
queries and vector store operations. It is a single class that manages 7
Types of memory with consistent read/write patterns.


| Memory Type | Storage | Write Method | Read Method |
|-------------|---------|--------------|-------------|
| **Conversational** | SQL Table | `write_conversational_memory()` | `read_conversational_memory()` |
| **Knowledge Base** | Vector Store | `write_knowledge_base()` | `read_knowledge_base()` |
| **Workflow** | Vector Store | `write_workflow()` | `read_workflow()` |
| **Toolbox** | Vector Store | `write_toolbox()` | `read_toolbox()` |
| **Entity** | Vector Store | `write_entity()` | `read_entity()` |
| **Summary** | Vector Store | `write_summary()` | `read_summary_memory()`, `read_summary_context()` |
| **Tool Log** | SQL Table | `write_tool_log()` | `read_tool_logs()` |

"""

"""
Define Memory Manager class here
"""

import os 
import sys 
import time 
import warnings
import logging
import oracledb 

from dotenv import load_dotenv, find_dotenv
from langchain_oracledb.vectorstores import OracleVS

from langchain_oracledb.retrievers.hybrid_search import OracleVectorizerPreference
from langchain_community.vectorstores.utils import DistanceStrategy
import json as json_lib

from datetime import datetime
import inspect

import uuid
from typing import Callable, Optional, Union
from pydantic import BaseModel


# Suppress warnings
import warnings
warnings.filterwarnings("ignore")


def load_env():
	load_dotenv(find_dotenv())


def suppress_warnings():
	# Huggingface / transformers log messages
	logging.getLogger("huggingface_hub").setLevel(logging.Error)
	logging.getLogger("transformers").setLevel(logging.Error)


def get_openai_api_key():
	load_env()
	openai_api_key = os.getenv("OPENAI_API_KEY")
	return openai_api_key


def setup_oracle_database(admin_user="system", admin_password="YourPassword123", dsn="127.0.0.1:1521/FREEPDB1",
                          vector_password="VectorPwd_2025"):
	"""
	One-time setup: configures tablespace and VECTOR user.


	Requires an admin user (e.g. system). This functon: 

	1. Connects as admin
	2. Finds an ASSM tablespace via USER_TABLESPACES (fix ORA-43853)
	3. Creates VECTOR user with required grants and ASSM default tablespace
	4. Tests connection as VECTOR
	"""
	print ("="* 60)
	print ("ORACLE DATABASE SETUP")
	print ("="*60)


	# Step 1: Connect as admin
	print("\n[1/4] Connecting as admin...")

	try:
        admin_conn = oracledb.connect(
            user=admin_user, password=admin_password, dsn=dsn
        )
        print(f"  Connected as {admin_user}")
    except Exception as e:
        print(f"  Admin connection failed: {e}")
        return False



     try:
        # Step 2: Find ASSM tablespace for JSON column support
        print("\n[2/4] Finding JSON-compatible (ASSM) tablespace...")
        assm_ts = _find_assm_tablespace(admin_conn)

        # Step 3: Create VECTOR user with ASSM default tablespace
        print("\n[3/4] Creating VECTOR user...")
        with admin_conn.cursor() as cur:
            ts_clause = (
                f"DEFAULT TABLESPACE {assm_ts}" if assm_ts else ""
            )
            cur.execute(f"""
                DECLARE
                    user_count NUMBER;
                BEGIN
                    SELECT COUNT(*) INTO user_count
                    FROM all_users WHERE username = 'VECTOR';
                    IF user_count = 0 THEN
                        EXECUTE IMMEDIATE
                            'CREATE USER VECTOR IDENTIFIED BY '
                            || '{vector_password} {ts_clause}';
                        EXECUTE IMMEDIATE
                            'GRANT CONNECT, RESOURCE, CREATE SESSION'
                            || ' TO VECTOR';
                        EXECUTE IMMEDIATE
                            'GRANT UNLIMITED TABLESPACE TO VECTOR';
                        EXECUTE IMMEDIATE
                            'GRANT CREATE TABLE, CREATE SEQUENCE,'
                            || ' CREATE VIEW TO VECTOR';
                    END IF;
                END;
            """)
            # Always set the default tablespace for VECTOR (even
            # if the user already existed from a previous run)
            if assm_ts:
                cur.execute(
                    f"ALTER USER VECTOR DEFAULT TABLESPACE"
                    f" {assm_ts}"
                )
        admin_conn.commit()
        if assm_ts:
            print(f"  VECTOR user ready "
                  f"(default tablespace: {assm_ts})")
        else:
            print("  VECTOR user created but no ASSM tablespace"
                  " found — JSON columns may fail (ORA-43853)")

    except Exception as e:
        print(f"  Warning during setup: {e}")
    finally:
        admin_conn.close()

    # Step 4: Test connection as VECTOR
    print("\n[4/4] Testing connection as VECTOR...")
    try:
        conn = oracledb.connect(
            user="VECTOR", password=vector_password, dsn=dsn
        )
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM dual")
            cur.fetchone()
        conn.close()
        print("  Connection successful!")
    except Exception as e:
        print(f"  Connection failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    print(f"""
You can now connect to Oracle:
    User: VECTOR
    Password: {vector_password}
    DSN: {dsn}
""")
    return True


def _find_assm_tablespace(conn):
    """
    Find an existing ASSM tablespace for JSON column support.

    Uses USER_TABLESPACES which is accessible to ANY Oracle user
    (no DBA privileges required). Prefers DATA > USERS > SYSAUX.
    Only attempts to CREATE a tablespace as a last resort.

    Returns the tablespace name or None.
    """
    # Step 1: Query USER_TABLESPACES for existing ASSM tablespaces
    # This view is available to every Oracle user — no DBA needed.
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT TABLESPACE_NAME
                FROM USER_TABLESPACES
                WHERE SEGMENT_SPACE_MANAGEMENT = 'AUTO'
                  AND STATUS = 'ONLINE'
                ORDER BY CASE TABLESPACE_NAME
                    WHEN 'DATA' THEN 1
                    WHEN 'USERS' THEN 2
                    WHEN 'SYSAUX' THEN 3
                    ELSE 4
                END
            """)
            row = cur.fetchone()
            if row:
                print(f"  Found ASSM tablespace: {row[0]}")
                return row[0]
    except Exception as e:
        print(f"  USER_TABLESPACES query failed: {e}")

    # Step 2: No ASSM tablespace found — try creating DATA
    # Try with OMF first, then with explicit path if possible
    create_sqls = [
        "CREATE TABLESPACE DATA"
        " DATAFILE SIZE 500M"
        " AUTOEXTEND ON NEXT 100M MAXSIZE UNLIMITED"
        " SEGMENT SPACE MANAGEMENT AUTO"
    ]
    # Try to discover datafile path for non-OMF installs
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT FILE_NAME FROM DBA_DATA_FILES"
                " FETCH FIRST 1 ROW ONLY"
            )
            row = cur.fetchone()
            if row:
                datafile_dir = os.path.dirname(row[0])
                create_sqls.insert(0,
                                   f"CREATE TABLESPACE DATA"
                                   f" DATAFILE '{datafile_dir}/data01.dbf'"
                                   f" SIZE 500M AUTOEXTEND ON NEXT 100M"
                                   f" MAXSIZE UNLIMITED"
                                   f" SEGMENT SPACE MANAGEMENT AUTO"
                                   )
    except Exception:
        pass

    for sql in create_sqls:
        try:
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
            print("  Created DATA tablespace (ASSM)")
            return 'DATA'
        except Exception as e:
            err = str(e)
            if "ORA-01543" in err:
                print("  DATA tablespace already exists")
                return 'DATA'
            continue

    print("  Could not find or create ASSM tablespace")
    return None


def connect_to_oracle(max_retries=3, retry_delay=5, user="system", password="YourPassword123",
                      dsn="127.0.0.1:1521/FREE", program="langchain_oracledb_deep_research_demo"):
    """
    Connect to Oracle database with retry logic and better error handling.

    Args:
        max_retries: Maximum number of connection attempts
        retry_delay: Seconds to wait between retries
    """

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Connection attempt {attempt}/{max_retries}...")
            conn = oracledb.connect(
                user=user,
                password=password,
                dsn=dsn,
                program=program
            )
            print("✓ Connected successfully!")

            # Test the connection
            with conn.cursor() as cur:
                try:
                    cur.execute("SELECT banner FROM v$version WHERE banner LIKE 'Oracle%';")
                    banner = cur.fetchone()[0]
                    print(f"\n{banner}")
                except Exception:
                    cur.execute("SELECT 1 FROM DUAL")
                    cur.fetchone()
                    print("  Connected to Oracle Database")

            return conn

        except oracledb.OperationalError as e:
            error_msg = str(e)
            print(f"✗ Connection failed (attempt {attempt}/{max_retries})")

            if "DPY-4011" in error_msg or "Connection reset by peer" in error_msg:
                print("  → This usually means:")
                print("    1. Database is still starting up (wait 2-3 minutes)")
                print("    2. Listener configuration issue")
                print("    3. Container is not running")

                if attempt < max_retries:
                    print(f"\n  Waiting {retry_delay} seconds before retry...")
                    time.sleep(retry_delay)
                else:
                    print("\n  💡 Try running: setup_oracle_database()")
                    print("     This will fix the listener and verify the connection.")
                    raise
            else:
                raise
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            raise

    raise ConnectionError("Failed to connect after all retries")



def table_exists(conn, table_name):
    """Check if a table exists in the current user's schema."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*) 
            FROM USER_TABLES 
            WHERE TABLE_NAME = UPPER(:table_name)
        """, {"table_name": table_name})
        return cur.fetchone()[0] > 0


def create_conversational_history_table(conn, table_name: str = "CONVERSATIONAL_MEMORY"):
    """
    Create a table to store conversational history.
    If the table already exists, returns the table name without recreating it.
    """
    # Check if table already exists
    if table_exists(conn, table_name):
        print(f"  ⏭️ Table {table_name} already exists (using existing table)")
        return table_name

    with conn.cursor() as cur:
        # Create table with proper schema
        cur.execute(f"""
            CREATE TABLE {table_name} (
                id VARCHAR2(100) DEFAULT SYS_GUID() PRIMARY KEY,
                thread_id VARCHAR2(100) NOT NULL,
                role VARCHAR2(50) NOT NULL,
                content CLOB NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata CLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                summary_id VARCHAR2(100) DEFAULT NULL
            )
        """)

        # Create index on thread_id for faster lookups
        cur.execute(f"""
            CREATE INDEX idx_{table_name.lower()}_thread_id ON {table_name}(thread_id)
        """)

        # Create index on timestamp for ordering
        cur.execute(f"""
            CREATE INDEX idx_{table_name.lower()}_timestamp ON {table_name}(timestamp)
        """)

    conn.commit()
    print(f"  ✅ Table {table_name} created successfully with indexes")
    return table_name


def create_tool_log_table(conn, table_name: str = "TOOL_LOG_MEMORY"):
    """
    Create a table to store raw tool execution logs per thread.
    If the table already exists, returns the table name without recreating it.
    """
    if table_exists(conn, table_name):
        print(f"  ⏭️ Table {table_name} already exists (using existing table)")
        return table_name

    with conn.cursor() as cur:
        cur.execute(f"""
            CREATE TABLE {table_name} (
                id VARCHAR2(100) DEFAULT SYS_GUID() PRIMARY KEY,
                thread_id VARCHAR2(100) NOT NULL,
                tool_call_id VARCHAR2(200),
                tool_name VARCHAR2(200) NOT NULL,
                tool_args CLOB,
                result CLOB,
                result_preview VARCHAR2(2000),
                status VARCHAR2(30) DEFAULT 'success',
                error_message CLOB,
                metadata CLOB,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cur.execute(f"""
            CREATE INDEX idx_{table_name.lower()}_thread_id ON {table_name}(thread_id)
        """)
        cur.execute(f"""
            CREATE INDEX idx_{table_name.lower()}_tool_name ON {table_name}(tool_name)
        """)
        cur.execute(f"""
            CREATE INDEX idx_{table_name.lower()}_timestamp ON {table_name}(timestamp)
        """)

    conn.commit()
    print(f"  ✅ Table {table_name} created successfully with indexes")
    return table_name


def safe_create_index(conn, vs, idx_name):
    """Create IVF vector index using raw SQL for maximum compatibility.

    Uses IVF (NEIGHBOR PARTITIONS) instead of HNSW to avoid:
    - ORA-00600 on some Oracle Free versions
    - ORA-51928 (DML not supported with INMEMORY NEIGHBOR GRAPH)
    - ORA-51962 (vector memory pool sizing issues)

    Handles ORA-00955 (index already exists) by skipping.
    """
    dist_map = {
        "COSINE": "COSINE",
        "EUCLIDEAN_DISTANCE": "EUCLIDEAN",
        "DOT_PRODUCT": "DOT",
    }
    dist = dist_map.get(vs.distance_strategy.name, "COSINE")

    try:
        with conn.cursor() as cur:
            cur.execute(
                f"CREATE VECTOR INDEX {idx_name}"
                f" ON {vs.table_name}(EMBEDDING)"
                f" ORGANIZATION NEIGHBOR PARTITIONS"
                f" DISTANCE {dist}"
                f" WITH TARGET ACCURACY 95"
            )
        print(f"  ✅ Created index: {idx_name}")
    except Exception as e:
        err = str(e)
        if "ORA-00955" in err:
            print(f"  ⏭️  Index already exists: {idx_name}")
        else:
            raise



def cleanup_vector_memory(conn, drop_tables: bool = False, table_prefix: str = None):
    """
    Clean up vector indexes and optionally tables to free up vector memory space.

    Use this when you encounter ORA-51962: vector memory area is out of space.

    Args:
        conn: Oracle database connection
        drop_tables: If True, also drops the vector tables (WARNING: deletes all data)
        table_prefix: If provided, only clean up tables/indexes matching this prefix
                      (e.g., "SEMANTIC" to only clean SEMANTIC_MEMORY)

    Returns:
        dict with counts of dropped indexes and tables
    """
    dropped_indexes = 0
    dropped_tables = 0

    print("=" * 60)
    print("🧹 CLEANING UP VECTOR MEMORY")
    print("=" * 60)

    with conn.cursor() as cur:
        # Find all vector indexes
        cur.execute("""
            SELECT INDEX_NAME, TABLE_NAME 
            FROM USER_INDEXES 
            WHERE INDEX_TYPE = 'VECTOR'
            ORDER BY TABLE_NAME
        """)
        indexes = cur.fetchall()

        if not indexes:
            print("  ℹ️ No vector indexes found")
        else:
            print(f"\n[1/2] Dropping vector indexes ({len(indexes)} found)...")
            for idx_name, table_name in indexes:
                # Apply prefix filter if specified
                if table_prefix and not table_name.upper().startswith(table_prefix.upper()):
                    continue
                try:
                    cur.execute(f"DROP INDEX {idx_name}")
                    print(f"  ✅ Dropped index: {idx_name} (on {table_name})")
                    dropped_indexes += 1
                except Exception as e:
                    print(f"  ⚠️ Failed to drop {idx_name}: {e}")
            conn.commit()

        if drop_tables:
            # Find vector tables (tables with VECTOR columns)
            cur.execute("""
                SELECT DISTINCT TABLE_NAME 
                FROM USER_TAB_COLUMNS 
                WHERE DATA_TYPE = 'VECTOR'
                ORDER BY TABLE_NAME
            """)
            tables = cur.fetchall()

            if not tables:
                print("  ℹ️ No vector tables found")
            else:
                print(f"\n[2/2] Dropping vector tables ({len(tables)} found)...")
                for (table_name,) in tables:
                    # Apply prefix filter if specified
                    if table_prefix and not table_name.upper().startswith(table_prefix.upper()):
                        continue
                    try:
                        cur.execute(f"DROP TABLE {table_name} PURGE")
                        print(f"  ✅ Dropped table: {table_name}")
                        dropped_tables += 1
                    except Exception as e:
                        print(f"  ⚠️ Failed to drop {table_name}: {e}")
                conn.commit()
        else:
            print("\n[2/2] Skipping table deletion (drop_tables=False)")
            print("  💡 Set drop_tables=True to also remove tables and free more space")

    print("\n" + "=" * 60)
    print(f"🎉 CLEANUP COMPLETE: {dropped_indexes} indexes, {dropped_tables} tables dropped")
    print("=" * 60)

    return {"indexes_dropped": dropped_indexes, "tables_dropped": dropped_tables}



def list_vector_objects(conn):
    """
    List all vector indexes and tables in the current schema.
    Useful for diagnosing space issues before cleanup.
    """
    print("=" * 60)
    print("📋 VECTOR OBJECTS IN SCHEMA")
    print("=" * 60)

    with conn.cursor() as cur:
        # List vector indexes
        cur.execute("""
            SELECT INDEX_NAME, TABLE_NAME, STATUS
            FROM USER_INDEXES 
            WHERE INDEX_TYPE = 'VECTOR'
            ORDER BY TABLE_NAME
        """)
        indexes = cur.fetchall()

        print(f"\n🔍 Vector Indexes ({len(indexes)}):")
        if indexes:
            for idx_name, table_name, status in indexes:
                print(f"  - {idx_name} on {table_name} [{status}]")
        else:
            print("  (none)")

        # List tables with vector columns
        cur.execute("""
            SELECT TABLE_NAME, COLUMN_NAME
            FROM USER_TAB_COLUMNS 
            WHERE DATA_TYPE = 'VECTOR'
            ORDER BY TABLE_NAME
        """)
        tables = cur.fetchall()

        print(f"\n📊 Tables with Vector Columns ({len(tables)}):")
        if tables:
            for table_name, col_name in tables:
                # Get row count
                try:
                    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cur.fetchone()[0]
                    print(f"  - {table_name}.{col_name} ({count:,} rows)")
                except:
                    print(f"  - {table_name}.{col_name}")
        else:
            print("  (none)")

    print("=" * 60)




"""
The class MemoryManager handles 
"""

class MemoryManager: 
	"""
	A simplified memory manager for AI Agents using
	Oracle AI database (extensible to other databases)

	Manages 7 types of memory: 
	- Conversational: Chat History per thread (SQL Table)
	- Tool Log: Raw tool execution outputs and metadata (SQL table)
	- Knowledge Base: Seachable documents (Vector Store)
	- Workflow: Execution Patterns (Vector Store)
	- Toolbox: Available Tools ()
	- Entity: People, places, systems (Vector Table)
	- Summary: Storing Compressed Context window
	"""

	def __init__(self,
        conn,
        conversational_table:str,
        knowledge_base_vs,
        workflow_vs,
        toolbox_vs,
        entity_vs,
        summary_vs,
        tool_log_table: str | None = None
        ):
		return None

        #iniitalise the different comoponents.
        self.conn = conn
        self.conversational_table= 
        self.knowledge_base_vs=
        self.workflow_vs=
        self.toolbox_vs=
        self.entity_vs=
        self.summary_vs=
        self.tool_log_table= tool_log_table



    #----------------- Conversational Memory (SQL)----------------#

    def write_conversational_memory(self,
        content:str,
        role:str,
        thread_id:str
        ):

        """Store a message in conversation history."""
        thread_id = str(thread_id)
        with self.conn.cursor() as cur:
            id_var = cur.var(str)
            cur.execute(f"""
                INSERT INTO {self.conversation_table} (thread_id, role, content, metadata, timestamp)
                VALUES (:thread_id, :role, :content, :metadata, CURRENT_TIMESTAMP)
                RETURNING id INTO :id
            """,{"thread_id":thread_id,
            "role":role,
            "content":content,
            "metadata":"{}",
            "id":id_var
            })
            record_id = id_var.
        return record_id
    
    def read_conversational_memory(
        self,
        thread_id:str,
        limit:int=10
        )-> str:

        """
        Read conversation history for a thread (excludes summarized messages.)
        """
        thread_id = str(thread_id) #type casting thread_id into string type

        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT role, content, timestamp FROM {self.conversation_table}
                WHERE thread_id = :thread_id AND summary_id IS NULL
                ORDER BY timestamp ASC
                FETCH FIRST :limit ROWS ONLY
            """, {"thread_id": thread_id, "limit": limit})
            results = cur.fetchall()

        messages = [f"[{ts.strftime('%H:%M:%S')}] [{role}] {content}" for role, content, ts in results]
        messages_formatted = '\n'.join(messages)
        if not messages_formatted:
            messages_formatted = "(No unsummarized messages found for this thread.)"
        return f"""## Conversation Memory
            ### What this memory is
            Chronological, unsummarized messages from the current thread. This memory captures user intent, constraints, and commitments made in recent turns.
            ### How you should leverage it
            - Preserve continuity with prior decisions, terminology, and user preferences.
            - Resolve references like "that", "previous step", or "the paper above" using earlier turns.
            - If older context conflicts with newer user instructions, prioritize the latest user direction.
            ### Retrieved messages

            {messages_formatted}"""



    ##### Tool Logs Memory ---------------------------------------
    def mark_as_summarized(self, thread_id: str, summary_id: str):
        """Mark all unsummarized messages in a thread as summarized."""
        thread_id = str(thread_id)
        with self.conn.cursor() as cur:
            cur.execute(f"""
                UPDATE {self.conversation_table}
                SET summary_id = :summary_id
                WHERE thread_id = :thread_id AND summary_id IS NULL
            """, {"summary_id": summary_id, "thread_id": thread_id})
        self.conn.commit()
        print(f"  📦 Marked messages as summarized (summary_id: {summary_id})")

        return None 



    ### TOOL LOG MEMORY(SQL)------------------#######
     def write_tool_log(
        self,
        thread_id:str,
        tool_name:str,
        tool_args:str,
        result:str,
        status:str = "success",
        tool_call_id: str | None = None,
        error_message: str | None = None,
        metadata: dict | None = None,
        ) ->str | None:

        """
        Persist raw tool execution logs for 
        auditing and just-in-time retrieval.
        """
        if not self.tool_log_table:
            return None

        thread_id = str(thread_id)


        if isinstance(tool_args, (dict, list)):
            tool_args_str = json_lib.dumps(tool_args, ensure_ascii=False)
        else:
            tool_args_str = "" if tool_args is None else str(tool_args)

        result_str = "" if result is None else str(result)
        # Oracle VARCHAR2(2000) may be byte-limited; truncate preview by UTF-8 bytes.
        preview = result_str.encode("utf-8")[:2000].decode("utf-8", errors="ignore")

        metadata_str = json_lib.dumps(metadata, ensure_ascii=False) if metadata else "{}"

        return None


    def read_tool_logs(self,
        thread_id:str,
        limit:int=20)-> list[dict]:

        """
        Read recent tool logs for a thread, newest first
        """
        if not self.tool_log_table:
            return []


        thread_id = str(thread_id)

        with self.conn.cursor() as cur: 
            cur.execute(f"""
                SELECT id, tool_call_id, tool_name, tool_args, result_preview, status, error_message, metadata, timestamp
                FROM {self.tool_log_table}
                WHERE thread_id = :thread_id
                ORDER BY timestamp DESC
                FETCH FIRST :limit ROWS ONLY
            """, {"thread_id": thread_id, "limit": limit})
            rows = cur.fetchall()


            logs = []

            for log_id, tool_call_id, tool_name, tool_args, result_preview, status, error_message, metadata, ts in rows:
            logs.append({
                "id": log_id,
                "tool_call_id": tool_call_id,
                "tool_name": tool_name,
                "tool_args": tool_args,
                "result_preview": result_preview,
                "status": status,
                "error_message": error_message,
                "metadata": metadata,
                "timestamp": ts.isoformat() if ts else None,
            })
        return logs

        return None

   

    def write_knowledge_base(
        self, text: str | list[str], metadata: dict | list[dict]
        ):

        """
        Knowledge Base is structured Data Repository,
        Supports: 
        - Single Record: text=str, metadata=dict
        - Batch_insert: test= list[str],metadata=list[dict]        
        """

        if instance(text,list):
            texts = [str(t) for t in text]

            if isinstance(metadata,list):
                metadatas = metadata
            else:
                metadatas = [metadata for _ in texts]

            #Goal: You wanna achieve for every text one metadata. 
            if len(texts) !=len(metadatas):
                raise ValueError(
                    f"knowledge-base batch length mismatch: {len(texts) } vs {len(metadatas)}metadata rows"
                    )
                self.knowledge_base_vs.add_texts(texts,metadatas)
        return self.knowledge_base_vs.add_texts([str(text)], [metadata if isinstance(metadata, dict) else {}])

    """
    Read_Knowledge Base: 
    self, query, k
    """
    def read_knowledge_base(self,query:str,k:int=3)->str:
        """
        Search Knowledge base for relevant content.
        """
        results = self.knowledge_base_vs.similarity(query,k=k)
        content = "\n".join([doc.page_content for doc in results])

        if not content:
            content = "(No relevant knowledge base passages found.)"
        return f"""## Knowledge Base Memory
        ### What ths memory is Retrieved background documents
        and previously ingested reference material relevant to the current query.

        ### How you should leverage it

        - Ground responses in these passages when making factunal or technical claims.
        - Prefer concrete details from this memory over unsupported
        assumptons. 

        - If evidence is missing or ambitious, state uncertainty and request clarification or 
        additional retrieval. 
        ### Retrieved Passages{content}
        """


    #----------------- WORKFLOW (Vector Store) ----------------#
    def write_workflow(
        self,
        query: str,
        steps:list, 
        final_answer:str, 
        success: bool = True
        ):
        """
        Store a completed workflow for future 
        reference.
        """


        # Format steps as text
        steps_text = "\n".join([f"Step {i + 1}: {s}" for i, s in enumerate(steps)])
        text = f"Query: {query}\nSteps:\n{steps_text}\nAnswer: {final_answer[:200]}"


        metadata = {
            "query": query,
            "success": success,
            "num_steps": len(steps),
            "timestamp": datetime.now().isoformat()
        }
        self.workflow_vs.add_texts([text], [metadata])

        return None

    def read_workflow(self,
        query:str,
        k:int = 3)-> str:
        """
        Search for similar past workflows with at least 1 step.
        """

        # Filter to only include workflows that have steps (num_steps >0 )
        results = self.workflow_vs.similarity_search(
            query,
            k=k,
            filter = {"num_steps":{"$gt":0}}
            )

        if not results: 
            return """## Workflow Memory
### What this memory is
Past task trajectories that include query context, ordered steps taken, and prior outcomes.
### How you should leverage it
- Use these workflows as reusable execution patterns for planning and tool orchestration.
- Adapt step sequences to the current task rather than copying blindly.
- Reuse successful patterns first, then adjust when task scope or constraints differ.
### Retrieved workflows
(No relevant workflows found.)"""
        content = "\n---\n".join([doc.page_content for doc in results])
        return f"""## Workflow Memory
### What this memory is
Past task trajectories that include query context, ordered steps taken, and prior outcomes.
### How you should leverage it
- Use these workflows as reusable execution patterns for planning and tool orchestration.
- Adapt step sequences to the current task rather than copying blindly.
- Reuse successful patterns first, then adjust when task scope or constraints differ.
### Retrieved workflows

{content}"""




        return None

    #----------------- Toolbox (Vector Store) ------------------#

    def write_toolbox(self):
        return None

    def read_toolbox(self):
        return None


    #----------------- Enttiy (Vector Store) -----------------#

    def extract_entities(self):
        return None

    def write_entity(self):
        return None

    def read_entity(self):
        return None


    #----------------- Summary (Vector Store) -----------------#
    def write_summary(self):
        return None


    def read_summary_memory(self):
        return None


    def read_summary_context(self, query: str = "", k: int = 10, thread_id: str | None = None) -> str:
        """Get available summaries for context window (IDs + descriptions only)."""
        filters = None
        if thread_id is not None:
            filters = {"thread_id": str(thread_id)}
        results = self.summary_vs.similarity_search(query or "summary", k=k, filter=filters)
        if not results:
            scope_note = (
                f"(No summaries available for thread {thread_id}.)"
                if thread_id is not None
                else "(No summaries available.)"
            )
            return """## Summary Memory
            ### What this memory is
            Compressed snapshots of older conversation windows preserved to retain long-range context.
            ### How you should leverage it
            - Use summaries to maintain continuity when full historical messages are not in the active context window.
            - Call expand_summary(id) before depending on exact quotes, fine-grained details, or step-by-step chronology.
            ### Available summaries
            """ + scope_note

        lines = [
            "## Summary Memory",
            "### What this memory is",
            "Compressed snapshots of older conversation windows preserved to retain long-range context.",
            "### How you should leverage it",
            "- Use summaries to maintain continuity when full historical messages are not in the active context window.",
            "- Call expand_summary(id) before depending on exact quotes, fine-grained details, or step-by-step chronology.",
            "### Available summaries",
            "Use expand_summary(id) to retrieve the detailed underlying conversation."
        ]
        if thread_id is not None:
            lines.append(f"Scope: thread_id = {thread_id}")
        for doc in results:
            sid = doc.metadata.get('id', '?')
            desc = doc.metadata.get('description', 'No description')
            lines.append(f"  • [ID: {sid}] {desc}")
        return "\n".join(lines) 


    def read_conversations_by_summary_id(self,
        summary_id:str
        )-> str:
        """
        Retrieve all original conversations that were summarized
        with a given summary_id

        Returns converstons in order of occurrence with timestamps.

        Args: 
            summary_id: The ID of the summary to expand

        Returns: 
            Formatted string with original conversations and timestamps
        """

         with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT id, role, content, timestamp 
                FROM {self.conversation_table}
                WHERE summary_id = :summary_id
                ORDER BY timestamp ASC
            """, {"summary_id": summary_id})
            results = cur.fetchall()


        ###########if not results found:
        if not results:
            return f"No conversations found for summary_id:{summary_id}"

        # Else: format conversations with timestamps
        lines = []
        lines.append(f"Total messages: {len(results)}\n")

        for msg_id, role, content, timestamp in results:
            ts_str = timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp else "Unknown"
            lines.append(f"[{ts_str}] [{role.upper()}]")
            lines.append(f"{content}")
            lines.append("")  # Empty line between messages

        return "\n".join(lines) 

        return None




"""
Define StoreManager because we have 
different DataBases for different Memories we 
need to build.
"""

class StoreManager:
	"""
	Manages all stoeres (vector stores and SQL Tables) with
	getter methods for easy access.
	"""

	def __init__(self,client,embedding_function,table_names,distance_strategy,conversational_talbe,tool_table: str | None = None):
		"""
		Initialize all stores

		Args: 
			client: Oracle database connection
			embedding_function: embedding model being used 
			table_names: Dict with keys: 
						knowledge_base,
						workflow, toolbox, 
						entiry,
						summary

			distance_strategy: Which distance function to use for the vector search
			conversational_table: Name of conversational history SQL table
			tool_log_talbe: Name of the SQL tool log table
		"""

		self.client = client
		self.embedding_function = embedding_function
		self.distance_strategy = distance_strategy
		self._conversational_table = conversational_table
		self._tool_log_table = tool_log_table


		# Initialize all vector stores for the different types of memory we have.
		self.knowledge_base_vs = OracleVS(
			client = client,
			embedding_function = embedding_function,
			table_name = table_names['knowledge_base'],
			distance_strategy=distance_strategy
			)
		
		self._workflow_vs = OracleVS(
			client = client,
			embedding_function = embedding_function,
			table_name = table_names['workflow'],
			distance_strategy=distance_strategy
			)
		
		self.toolbox_vs = OracleVS(
			client = client,
			embedding_function = embedding_function,
			table_name = table_names['toolbox'],
			distance_strategy=distance_strategy
			)
		
		self._entity_vs = OracleVS(
			client = client,
			embedding_function=embedding_function,
			table_name = table_names['entity'],
			distance_strategy = distance_strategy
			)
		
		self._summary_vs = OracleVS(
			client = client,
			embedding_function=embedding_function,
			table_name=table_names['summary'],
			distance_strategy = distance_strategy
			)

		# Store Hybrid search preference for knowledge base(optional)
		self._kb_vectorizer_pref = None

		
		# Add Getter Functions for the 		

		# Add the functions for Qdrant also here TO BE DEVELOPED
		self.knowledge_base_qdrant = None
		self._workflow_qdrant = None
		self._toolbox_qdrant = None
		self._entity_qdrant = None
		self._summary_qdrant = None

		self._kb_vectorizer_pref_qdrant = None


		def get_conversational_table(self):
			"""
			Return the conversational history table name
			"""
			return self._conversational_table

		def get_tool_log_table(self):
			"""

			"""
			return self._tool_log_table


		def get_knowledge_base_store(self):
			return self._knowledge_base_vs

		def get_workflow_store(self):
			"""
			Return the workflow vector store
			"""
			return self._workflow_vs

		def get_entity_store(self):
			"""
			Return the entity vector store
			"""
			return self._entity_vs


		def get_summary_store(self):
			"""
			Return the summary vector store 
			"""
			return self._summary_vs


		def setup_hybrid_search(self,preference_name="KB_VECTORIZER_PREF"):
			"""
			Set up hybrid search for knowledge base.
			Creates vectorizer preference for hybrid indexing.
			"""
			self._kb_vectorizer_pref = OracleVectorizerPreference.create_preference(

				vector_store = self._knowledge_base_vs,
				preference_name = preference_name
				)
			return self._kb_vectorizer_pref





###### 
#if we need Toolbox we can make 
######


##Deploy this by the evening the Memory Manager

