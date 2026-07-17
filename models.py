# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class TrackingResult(db.Model):
    __tablename__ = 'tracking_results'
    
    id = db.Column(db.Integer, primary_key=True)
    kode_resi = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50))
    status_terakhir = db.Column(db.String(200))
    nama = db.Column(db.String(100))
    hp = db.Column(db.String(20))
    paket = db.Column(db.String(500))
    nilai = db.Column(db.String(50))
    pesan_wa = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'kode_resi': self.kode_resi,
            'status': self.status,
            'status_terakhir': self.status_terakhir,
            'nama': self.nama,
            'hp': self.hp,
            'paket': self.paket,
            'nilai': self.nilai,
            'pesan_wa': self.pesan_wa,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }