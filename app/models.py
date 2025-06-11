from flask_login import UserMixin
from app import db

# Tabel Role
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship('User', backref='role', lazy=True)

# Tabel User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    nim = db.Column(db.String(20), unique=True, nullable=False)
    jurusan = db.Column(db.String(50), nullable=False)

class Dosen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    nip = db.Column(db.String(30), nullable=False, unique=True)
    prodi = db.Column(db.String(100), nullable=False)

class MataKuliah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(10), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    sks = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<MataKuliah {self.kode} - {self.nama}>'

class Jadwal(db.Model):
    __tablename__ = 'jadwal'

    id = db.Column(db.Integer, primary_key=True)
    mahasiswa_id = db.Column(db.Integer, db.ForeignKey('mahasiswa.id'), nullable=False)
    dosen_id = db.Column(db.Integer, db.ForeignKey('dosen.id'), nullable=False)
    mata_kuliah = db.Column(db.String(100), nullable=False)
    hari = db.Column(db.String(20), nullable=False)
    jam_mulai = db.Column(db.Time, nullable=False)
    jam_selesai = db.Column(db.Time, nullable=False)
    mahasiswa = db.relationship('Mahasiswa', backref='jadwal')
    dosen = db.relationship('Dosen', backref='jadwal')