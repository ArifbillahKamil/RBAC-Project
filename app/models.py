from flask_login import UserMixin
from app import db

# Tabel Role
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

# Tabel User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='users')

class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    nim = db.Column(db.String(20), unique=True, nullable=False)
    jurusan = db.Column(db.String(50), nullable=False)

class Dosen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    nip = db.Column(db.String(50), unique=True)
    prodi = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # <--- ini WAJIB ADA

class MataKuliah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kode_mk = db.Column(db.String(20))   # kolom sesuai database
    nama_mk = db.Column(db.String(100))  # kolom sesuai database
    kode = db.Column(db.String(20))      # kolom baru (jika ada)
    nama = db.Column(db.String(100))     # kolom baru (jika ada)
    sks = db.Column(db.Integer)

    def __repr__(self):
        return f'<MataKuliah {self.kode} - {self.nama}>'

class Jadwal(db.Model):
    __tablename__ = 'jadwal'

    id = db.Column(db.Integer, primary_key=True)
    mahasiswa_id = db.Column(db.Integer, db.ForeignKey('mahasiswa.id'), nullable=False)
    dosen_id = db.Column(db.Integer, db.ForeignKey('dosen.id'), nullable=False)
    hari = db.Column(db.String(20), nullable=False)
    jam_mulai = db.Column(db.Time, nullable=False)
    jam_selesai = db.Column(db.Time, nullable=False)
    mata_kuliah_id = db.Column(db.Integer, db.ForeignKey('mata_kuliah.id'), nullable=False)

    mahasiswa = db.relationship('Mahasiswa', backref='jadwal')
    dosen = db.relationship('Dosen', backref='jadwal')
    mata_kuliah = db.relationship('MataKuliah', backref='jadwal')

class MataKuliahJadwal(db.Model):
    __tablename__ = 'mata_kuliah_jadwal'

    id = db.Column(db.Integer, primary_key=True)
    jadwal_id = db.Column(db.Integer, db.ForeignKey('jadwal.id'), nullable=False)
    mata_kuliah_id = db.Column(db.Integer, db.ForeignKey('mata_kuliah.id'), nullable=False)

    jadwal = db.relationship('Jadwal', backref='mata_kuliah_jadwal')
    mata_kuliah = db.relationship('MataKuliah', backref='mata_kuliah_jadwal')