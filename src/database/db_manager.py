"""
Database Manager Module (SQLite)
Handles persistent storage of inspection sessions, defect detections,
geo-coordinates, and distress ratings for auditing and reporting.
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

DB_PATH = Path("inspection_database.db")

class DatabaseManager:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_tables()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_tables(self):
        """Create database tables if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Inspection Sessions table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS inspections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_name TEXT,
                image_name TEXT,
                timestamp TEXT,
                condition_score REAL,
                rating TEXT,
                total_defects INTEGER,
                latitude REAL,
                longitude REAL,
                original_image_path TEXT,
                annotated_image_path TEXT
            )
            """)
            
            # 2. Defect Detections table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS defects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inspection_id INTEGER,
                class_id INTEGER,
                class_name TEXT,
                confidence REAL,
                severity TEXT,
                area_ratio REAL,
                aspect_ratio REAL,
                bbox_x1 REAL,
                bbox_y1 REAL,
                bbox_x2 REAL,
                bbox_y2 REAL,
                crop_path TEXT,
                FOREIGN KEY(inspection_id) REFERENCES inspections(id) ON DELETE CASCADE
            )
            """)
            conn.commit()

    def insert_inspection(
        self,
        session_name: str,
        image_name: str,
        condition_score: float,
        rating: str,
        total_defects: int,
        latitude: float,
        longitude: float,
        original_image_path: str,
        annotated_image_path: str,
        defects_list: List[Dict]
    ) -> int:
        """Insert a full inspection event and its detected defects atomically."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO inspections (
                session_name, image_name, timestamp, condition_score, rating,
                total_defects, latitude, longitude, original_image_path, annotated_image_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_name, image_name, timestamp, condition_score, rating,
                total_defects, latitude, longitude, original_image_path, annotated_image_path
            ))
            inspection_id = cursor.lastrowid
            
            for d in defects_list:
                cursor.execute("""
                INSERT INTO defects (
                    inspection_id, class_id, class_name, confidence, severity,
                    area_ratio, aspect_ratio, bbox_x1, bbox_y1, bbox_x2, bbox_y2, crop_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    inspection_id,
                    d.get("class_id", 0),
                    d.get("class_name", "Damage"),
                    d.get("confidence", 0.0),
                    d.get("severity", "Minor"),
                    d.get("area_ratio", 0.0),
                    d.get("aspect_ratio", 0.0),
                    d.get("bbox", [0, 0, 0, 0])[0],
                    d.get("bbox", [0, 0, 0, 0])[1],
                    d.get("bbox", [0, 0, 0, 0])[2],
                    d.get("bbox", [0, 0, 0, 0])[3],
                    d.get("crop_path", "")
                ))
            conn.commit()
            return inspection_id

    def get_all_inspections(self) -> List[Dict]:
        """Fetch all inspection history records."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inspections ORDER BY id DESC")
            return [dict(row) for row in cursor.fetchall()]

    def get_defects_by_inspection(self, inspection_id: int) -> List[Dict]:
        """Fetch all defect detections belonging to a specific inspection ID."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
            SELECT * FROM defects WHERE inspection_id = ? ORDER BY id ASC
            """, (inspection_id,))
            return [dict(row) for row in cursor.fetchall()]

    def get_all_defects_with_geo(self) -> List[Dict]:
        """Fetch all defect detections joined with inspection GPS coordinates."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
            SELECT 
                d.id, d.inspection_id, d.class_name, d.confidence, d.severity, d.area_ratio, d.crop_path,
                i.latitude, i.longitude, i.timestamp, i.image_name
            FROM defects d
            JOIN inspections i ON d.inspection_id = i.id
            ORDER BY d.id DESC
            """)
            return [dict(row) for row in cursor.fetchall()]

    def get_kpi_metrics(self) -> Dict:
        """Calculate executive KPI counters for dashboard display."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM inspections")
            total_inspections = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM defects")
            total_defects = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM defects WHERE class_id = 3")
            total_potholes = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM defects WHERE class_id IN (0, 1, 2)")
            total_cracks = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM defects WHERE severity = 'Critical'")
            critical_alerts = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(condition_score) FROM inspections")
            avg_score = cursor.fetchone()[0] or 100.0
            
            return {
                "total_inspections": total_inspections,
                "total_defects": total_defects,
                "total_potholes": total_potholes,
                "total_cracks": total_cracks,
                "critical_alerts": critical_alerts,
                "avg_condition_score": round(avg_score, 1)
            }

