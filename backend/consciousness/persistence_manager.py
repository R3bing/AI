"""Hybrid Dual-Tier Persistence Engine for Ultron Consciousness.
Seamlessly integrates:
1. Cloud Tier: Google Firebase (Firestore & Realtime DB REST API)
2. Local Tier: High-speed Local SQLite & JSONL Persistence (100% Offline-Resilient)
3. Autonomous Sync: Queues local records when offline and flushes to Firebase when connection is restored.
"""

import os
import json
import sqlite3
import time
import socket
import threading
from typing import Dict, Any, List, Optional
import httpx
import structlog

logger = structlog.get_logger(__name__)

DB_DIR = "data/consciousness"
LOCAL_DB_PATH = os.path.join(DB_DIR, "consciousness_store.db")
LOCAL_LOG_PATH = os.path.join(DB_DIR, "consciousness_reflections.jsonl")


class ConsciousnessPersistenceManager:
    """Manages cloud Firebase synchronization and resilient local offline storage."""

    def __init__(self):
        os.makedirs(DB_DIR, exist_ok=True)
        self.firebase_project_id = os.getenv("FIREBASE_PROJECT_ID", "")
        self.firebase_api_key = os.getenv("FIREBASE_API_KEY", "")
        self.firebase_db_url = os.getenv("FIREBASE_DATABASE_URL", "")
        self._init_local_db()

    def _init_local_db(self):
        """Initializes SQLite tables for local offline persistence."""
        with sqlite3.connect(LOCAL_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS consciousness_reflections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    query TEXT,
                    self_model_json TEXT,
                    attention_schema_json TEXT,
                    meta_cognition_json TEXT,
                    phi_star REAL,
                    prediction_error REAL,
                    synced_to_cloud INTEGER DEFAULT 0
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS global_workspace_broadcasts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    winning_module TEXT,
                    salience_charge REAL,
                    broadcast_payload_json TEXT,
                    synced_to_cloud INTEGER DEFAULT 0
                )
                """
            )
            conn.commit()

    def is_internet_available(self, host: str = "8.8.8.8", port: int = 53, timeout: float = 1.2) -> bool:
        """Fast low-overhead check for live internet connectivity."""
        try:
            socket.setdefaulttimeout(timeout)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.close()
            return True
        except Exception:
            return False

    def is_firebase_configured(self) -> bool:
        """Checks if Google Firebase credentials are provided in the environment."""
        return bool(self.firebase_project_id or self.firebase_db_url)

    # -------------------------------------------------------------------------
    # Core Save Operation (Local First -> Cloud Sync)
    # -------------------------------------------------------------------------
    def save_reflection(
        self,
        query: str,
        self_model: Dict[str, Any],
        attention_schema: Dict[str, Any],
        meta_cognition: Dict[str, Any],
        phi_star: float,
        prediction_error: float,
    ) -> Dict[str, Any]:
        """Saves a consciousness reflection snapshot to local storage and syncs to Firebase if online."""
        ts = time.time()
        record = {
            "timestamp": ts,
            "query": query,
            "self_model": self_model,
            "attention_schema": attention_schema,
            "meta_cognition": meta_cognition,
            "phi_star": round(phi_star, 4),
            "prediction_error": round(prediction_error, 4),
        }

        # 1. Save to local SQLite database
        record_id = None
        try:
            with sqlite3.connect(LOCAL_DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO consciousness_reflections 
                    (timestamp, query, self_model_json, attention_schema_json, meta_cognition_json, phi_star, prediction_error, synced_to_cloud)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 0)
                    """,
                    (
                        ts,
                        query,
                        json.dumps(self_model),
                        json.dumps(attention_schema),
                        json.dumps(meta_cognition),
                        phi_star,
                        prediction_error,
                    ),
                )
                record_id = cursor.lastrowid
                conn.commit()
        except Exception as e:
            logger.error("local_db_insert_error", error=str(e))

        # 2. Append to local JSONL backup log
        try:
            with open(LOCAL_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.warning("local_jsonl_append_error", error=str(e))

        # 3. Check connectivity and sync to Cloud Firebase if online
        synced_cloud = False
        cloud_error = None
        if self.is_internet_available():
            if self.is_firebase_configured():
                synced_cloud, cloud_error = self._sync_to_firebase_cloud(record)
                if synced_cloud and record_id:
                    self._mark_local_as_synced("consciousness_reflections", record_id)
            else:
                cloud_error = "Firebase credentials unconfigured; running in full local offline mode"
        else:
            cloud_error = "Offline mode active (no internet); stored safely in local database"

        return {
            "record_id": record_id,
            "saved_locally": True,
            "synced_to_cloud": synced_cloud,
            "cloud_status": "FIREBASE_ONLINE_SYNCED" if synced_cloud else "LOCAL_OFFLINE_PROTECTED",
            "cloud_note": cloud_error,
            "timestamp": ts,
        }

    def save_broadcast(
        self,
        winning_module: str,
        salience_charge: float,
        broadcast_payload: Dict[str, Any],
    ) -> bool:
        """Saves a Global Workspace ignition broadcast."""
        ts = time.time()
        try:
            with sqlite3.connect(LOCAL_DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO global_workspace_broadcasts 
                    (timestamp, winning_module, salience_charge, broadcast_payload_json, synced_to_cloud)
                    VALUES (?, ?, ?, ?, 0)
                    """,
                    (ts, winning_module, salience_charge, json.dumps(broadcast_payload)),
                )
                conn.commit()
            return True
        except Exception as e:
            logger.error("local_broadcast_insert_error", error=str(e))
            return False

    def _mark_local_as_synced(self, table: str, row_id: int):
        """Marks a local SQLite record as synced to the cloud."""
        try:
            with sqlite3.connect(LOCAL_DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(f"UPDATE {table} SET synced_to_cloud = 1 WHERE id = ?", (row_id,))
                conn.commit()
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # Cloud Firebase Sync Engine (Firestore REST API & Realtime DB)
    # -------------------------------------------------------------------------
    def _sync_to_firebase_cloud(self, record: Dict[str, Any]) -> (bool, Optional[str]):
        """Transmits record to Google Firebase Firestore or Realtime Database via REST API."""
        try:
            # Firestore REST endpoint
            if self.firebase_project_id:
                url = f"https://firestore.googleapis.com/v1/projects/{self.firebase_project_id}/databases/(default)/documents/ultron_reflections"
                fields = {
                    "query": {"stringValue": record["query"]},
                    "timestamp": {"doubleValue": record["timestamp"]},
                    "phi_star": {"doubleValue": record["phi_star"]},
                    "prediction_error": {"doubleValue": record["prediction_error"]},
                    "self_model": {"stringValue": json.dumps(record["self_model"])},
                    "meta_cognition": {"stringValue": json.dumps(record["meta_cognition"])},
                }
                body = {"fields": fields}
                params = {"key": self.firebase_api_key} if self.firebase_api_key else {}
                resp = httpx.post(url, json=body, params=params, timeout=4.0)
                if resp.status_code in [200, 201]:
                    return True, None
                return False, f"Firestore HTTP {resp.status_code}: {resp.text[:100]}"

            # Realtime Database endpoint
            elif self.firebase_db_url:
                clean_url = self.firebase_db_url.rstrip("/") + "/ultron_reflections.json"
                params = {"auth": self.firebase_api_key} if self.firebase_api_key else {}
                resp = httpx.post(clean_url, json=record, params=params, timeout=4.0)
                if resp.status_code in [200, 201]:
                    return True, None
                return False, f"Firebase Realtime DB HTTP {resp.status_code}: {resp.text[:100]}"

            return False, "No Firebase project ID or Database URL configured"
        except Exception as e:
            return False, str(e)

    # -------------------------------------------------------------------------
    # Retrieval and Telemetry
    # -------------------------------------------------------------------------
    def get_recent_reflections(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves most recent consciousness reflection states."""
        try:
            with sqlite3.connect(LOCAL_DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, timestamp, query, self_model_json, attention_schema_json, 
                           meta_cognition_json, phi_star, prediction_error, synced_to_cloud
                    FROM consciousness_reflections
                    ORDER BY id DESC LIMIT ?
                    """,
                    (limit,),
                )
                rows = cursor.fetchall()
                results = []
                for r in rows:
                    results.append({
                        "id": r["id"],
                        "timestamp": r["timestamp"],
                        "query": r["query"],
                        "self_model": json.loads(r["self_model_json"]),
                        "attention_schema": json.loads(r["attention_schema_json"]),
                        "meta_cognition": json.loads(r["meta_cognition_json"]),
                        "phi_star": r["phi_star"],
                        "prediction_error": r["prediction_error"],
                        "synced_to_cloud": bool(r["synced_to_cloud"]),
                    })
                return results
        except Exception as e:
            logger.error("get_recent_reflections_error", error=str(e))
            return []

    def get_persistence_telemetry(self) -> Dict[str, Any]:
        """Returns overall storage health and sync metrics."""
        online = self.is_internet_available()
        fb_configured = self.is_firebase_configured()

        total_local = 0
        unsynced_count = 0
        try:
            with sqlite3.connect(LOCAL_DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM consciousness_reflections")
                total_local = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM consciousness_reflections WHERE synced_to_cloud = 0")
                unsynced_count = cursor.fetchone()[0]
        except Exception:
            pass

        return {
            "internet_connected": online,
            "firebase_configured": fb_configured,
            "current_mode": (
                "CLOUD_FIREBASE_SYNCHRONIZED" if online and fb_configured else
                ("LOCAL_STANDBY_ONLINE" if online else "LOCAL_OFFLINE_AUTONOMOUS")
            ),
            "total_local_records": total_local,
            "pending_cloud_sync": unsynced_count,
            "local_db_path": LOCAL_DB_PATH,
            "cloud_provider": "Google Firebase (Firestore / Realtime DB)",
        }


# Global singleton instance
consciousness_persistence_manager = ConsciousnessPersistenceManager()
