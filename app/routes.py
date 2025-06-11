from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Mahasiswa, User, Role, db, Dosen, MataKuliah, Jadwal

main = Blueprint('main', __name__)
dosen_bp = Blueprint('dosen', __name__, url_prefix='/admin/dosen')
admin_jadwal = Blueprint('admin_jadwal', __name__, url_prefix='/admin/jadwal')

# --- ROUTE DOSEN ---
@dosen_bp.route('/')
@login_required
def manage_dosen():
    if current_user.role.name != 'admin':
        return "Akses ditolak", 403
    dosen = Dosen.query.all()
    return render_template('dosen.html', dosen=dosen)

@dosen_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_dosen():
    if current_user.role.name != 'admin':
        return "Akses ditolak", 403

    if request.method == 'POST':
        nama = request.form['nama']
        nip = request.form['nip']
        prodi = request.form['prodi']

        existing = Dosen.query.filter_by(nip=nip).first()
        if existing:
            flash('NIP sudah terpakai!', 'danger')
            return redirect(url_for('dosen.add_dosen'))

        new_dosen = Dosen(nama=nama, nip=nip, prodi=prodi)
        db.session.add(new_dosen)
        db.session.commit()
        flash('Dosen berhasil ditambahkan.', 'success')
        return redirect(url_for('dosen.manage_dosen'))

    return render_template('add_dosen.html')

@dosen_bp.route('/edit/<int:dosen_id>', methods=['GET', 'POST'])
@login_required
def edit_dosen(dosen_id):
    if current_user.role.name != 'admin':
        return "Akses ditolak", 403

    dosen = Dosen.query.get_or_404(dosen_id)

    if request.method == 'POST':
        nama = request.form['nama']
        nip = request.form['nip']
        prodi = request.form['prodi']

        existing = Dosen.query.filter(Dosen.nip == nip, Dosen.id != dosen.id).first()
        if existing:
            flash('NIP sudah digunakan!', 'danger')
            return redirect(url_for('dosen.edit_dosen', dosen_id=dosen.id))

        dosen.nama = nama
        dosen.nip = nip
        dosen.prodi = prodi
        db.session.commit()
        flash('Dosen berhasil diupdate.', 'success')
        return redirect(url_for('dosen.manage_dosen'))

    return render_template('edit_dosen.html', dosen=dosen)

@dosen_bp.route('/delete/<int:dosen_id>', methods=['POST'])
@login_required
def delete_dosen(dosen_id):
    if current_user.role.name != 'admin':
        return "Akses ditolak", 403

    dosen = Dosen.query.get_or_404(dosen_id)
    db.session.delete(dosen)
    db.session.commit()
    flash('Dosen berhasil dihapus.', 'success')
    return redirect(url_for('dosen.manage_dosen'))

# --- ROUTE JADWAL ---
@admin_jadwal.route('/')
@login_required
def list_jadwal():
    jadwals = Jadwal.query.all()
    return render_template('jadwal_list.html', jadwals=jadwals)

@admin_jadwal.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah_jadwal():
    if request.method == 'POST':
        mahasiswa_id = request.form['mahasiswa_id']
        dosen_id = request.form['dosen_id']
        mata_kuliah_id = request.form['mata_kuliah_id']
        hari = request.form['hari']
        jam_mulai = request.form['jam_mulai']
        jam_selesai = request.form['jam_selesai']

        if jam_selesai <= jam_mulai:
            flash('Jam selesai harus lebih besar dari jam mulai!', 'error')
            return redirect(url_for('admin_jadwal.tambah_jadwal'))

        jadwal = Jadwal(
            mahasiswa_id=mahasiswa_id,
            dosen_id=dosen_id,
            mata_kuliah_id=mata_kuliah_id,
            hari=hari,
            jam_mulai=jam_mulai,
            jam_selesai=jam_selesai
        )
        db.session.add(jadwal)
        db.session.commit()
        flash('Jadwal berhasil ditambahkan!')
        return redirect(url_for('admin_jadwal.list_jadwal'))

    mahasiswas = Mahasiswa.query.all()
    dosens = Dosen.query.all()
    mata_kuliah = MataKuliah.query.all()
    return render_template(
        'jadwal_form.html',
        jadwal=None,
        mahasiswas=mahasiswas,
        dosens=dosens,
        mata_kuliah=mata_kuliah,
        action='tambah'
    )

@admin_jadwal.route('/edit/<int:jadwal_id>', methods=['GET', 'POST'])
@login_required
def edit_jadwal(jadwal_id):
    jadwal = Jadwal.query.get_or_404(jadwal_id)

    if request.method == 'POST':
        jadwal.mahasiswa_id = request.form['mahasiswa_id']
        jadwal.dosen_id = request.form['dosen_id']
        jadwal.mata_kuliah_id = request.form['mata_kuliah_id']
        jadwal.hari = request.form['hari']
        jadwal.jam_mulai = request.form['jam_mulai']
        jadwal.jam_selesai = request.form['jam_selesai']

        if jadwal.jam_selesai <= jadwal.jam_mulai:
            flash('Jam selesai harus lebih besar dari jam mulai!', 'error')
            return redirect(url_for('admin_jadwal.edit_jadwal', jadwal_id=jadwal.id))

        db.session.commit()
        flash('Jadwal berhasil diperbarui!')
        return redirect(url_for('admin_jadwal.list_jadwal'))

    mahasiswas = Mahasiswa.query.all()
    dosens = Dosen.query.all()
    mata_kuliah = MataKuliah.query.all()
    return render_template(
        'jadwal_form.html',
        jadwal=jadwal,
        mahasiswas=mahasiswas,
        dosens=dosens,
        mata_kuliah=mata_kuliah,
        action='edit'
    )

@admin_jadwal.route('/hapus/<int:jadwal_id>', methods=['POST', 'GET'])
@login_required
def hapus_jadwal(jadwal_id):
    jadwal = Jadwal.query.get_or_404(jadwal_id)
    db.session.delete(jadwal)
    db.session.commit()
    flash('Jadwal berhasil dihapus.')
    return redirect(url_for('admin_jadwal.list_jadwal'))

# --- ROUTE MAIN (users, roles, mahasiswa, dll) tetap seperti sebelumnya ---
@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name == 'admin':
        return render_template('dashboard.html', user=current_user)
    elif current_user.role.name == 'user':
        return "Kamu user biasa, akses dibatasi!"
    else:
        return "Role tidak dikenali!"

@main.route('/admin/users')
@login_required
def manage_users():
    if current_user.role.name != 'admin':
        return "Akses ditolak. Hanya admin yang bisa mengakses halaman ini.", 403

    from .models import User
    users = User.query.all()
    return render_template('manage_users.html', users=users)


# Tambah user - form
@main.route('/admin/users/add', methods=['GET'])
@login_required
def add_user_form():
    if current_user.role.name != 'admin':
        return "Akses ditolak!"
    
    from .models import Role
    roles = Role.query.all()
    return render_template('add_user.html', roles=roles)

# Tambah user - submit form
@main.route('/admin/users/add', methods=['POST'])
@login_required
def add_user():
    if current_user.role.name != 'admin':
        return "Akses ditolak!"

    email = request.form.get('email')
    password = request.form.get('password')
    role_id = int(request.form.get('role_id'))

    if not email or not password or not role_id:
        flash("Semua field harus diisi")
        return redirect(url_for('main.add_user_form'))

    from werkzeug.security import generate_password_hash
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    from .models import User, db
    new_user = User(email=email, password=hashed_password, role_id=role_id)
    db.session.add(new_user)
    db.session.commit()
    flash('User berhasil ditambahkan')
    return redirect(url_for('main.manage_users'))

@main.route('/admin/users/edit/<int:user_id>', methods=['GET'])
@login_required
def edit_user_form(user_id):
    if current_user.role.name != 'admin':
        return "Akses ditolak!", 403

    from .models import User, Role
    user = User.query.get_or_404(user_id)
    roles = Role.query.all()
    return render_template('edit_user.html', user=user, roles=roles)

@main.route('/admin/users/edit/<int:user_id>', methods=['POST'])
@login_required
def edit_user(user_id):
    if current_user.role.name != 'admin':
        return "Akses ditolak!", 403

    from .models import User, db
    user = User.query.get_or_404(user_id)

    email = request.form.get('email')
    role_id = request.form.get('role_id')

    user.email = email
    user.role_id = role_id
    db.session.commit()

    flash('User berhasil diperbarui.')
    return redirect(url_for('main.manage_users'))

@main.route('/admin/users/delete/<int:user_id>', methods=['POST', 'GET'])
@login_required
def delete_user(user_id):
    if current_user.role.name != 'admin':
        return "Akses ditolak!"

    from .models import User
    user = User.query.get_or_404(user_id)

    # Cegah admin menghapus dirinya sendiri
    if user.id == current_user.id:
        flash("Kamu tidak bisa menghapus akunmu sendiri.")
        return redirect(url_for('main.manage_users'))

    from .models import db
    db.session.delete(user)
    db.session.commit()
    flash('User berhasil dihapus.')
    return redirect(url_for('main.manage_users'))

@main.route('/admin/roles')
@login_required
def manage_roles():
    if current_user.role.name != 'admin':
        return "Akses ditolak!", 403

    from .models import Role
    roles = Role.query.all()
    return render_template('manage_roles.html', roles=roles)

@main.route('/admin/roles/add', methods=['GET', 'POST'])
@login_required
def add_role_form():
    if current_user.role.name != 'admin':
        return "Akses ditolak!", 403

    from .models import Role, db
    if request.method == 'POST':
        role_name = request.form['name']
        new_role = Role(name=role_name)
        db.session.add(new_role)
        db.session.commit()
        return redirect(url_for('main.manage_roles'))

    return render_template('add_role.html')

@main.route('/admin/roles/edit/<int:role_id>', methods=['GET', 'POST'])
@login_required
def edit_role_form(role_id):
    if current_user.role.name != 'admin':
        return "Akses ditolak!", 403

    from .models import Role, db
    role = Role.query.get_or_404(role_id)

    if request.method == 'POST':
        role.name = request.form['name']
        db.session.commit()
        flash('Role berhasil diperbarui.')
        return redirect(url_for('main.manage_roles'))

    return render_template('edit_role.html', role=role)


@main.route('/admin/roles/delete/<int:role_id>', methods=['GET', 'POST'])
@login_required
def delete_role(role_id):
    if current_user.role.name != 'admin':
        return "Akses ditolak!", 403

    from .models import Role, User, db
    role = Role.query.get_or_404(role_id)

    # Cek apakah role sedang digunakan oleh user lain
    if role.users:
        flash("Role tidak bisa dihapus karena sedang digunakan oleh user.")
        return redirect(url_for('main.manage_roles'))

    db.session.delete(role)
    db.session.commit()
    flash('Role berhasil dihapus.')
    return redirect(url_for('main.manage_roles'))

@main.route('/admin/mahasiswa')
@login_required
def manage_mahasiswa():
    if current_user.role.name != 'admin':
        return "Akses ditolak!", 403

    # Ambil query dari parameter GET
    search_query = request.args.get('q', '')

    if search_query:
        # Filter berdasarkan nama, nim, atau jurusan (case insensitive)
        mahasiswa = Mahasiswa.query.filter(
            (Mahasiswa.nama.ilike(f'%{search_query}%')) |
            (Mahasiswa.nim.ilike(f'%{search_query}%')) |
            (Mahasiswa.jurusan.ilike(f'%{search_query}%'))
        ).all()
    else:
        mahasiswa = Mahasiswa.query.all()

    return render_template('manage_mahasiswa.html', mahasiswa=mahasiswa, search_query=search_query)



@main.route('/admin/mahasiswa/add', methods=['GET', 'POST'])
@login_required
def add_mahasiswa():
    if current_user.role.name != 'admin':
        return "Akses ditolak!", 403

    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']
        jurusan = request.form['jurusan']

        # Cek apakah NIM sudah ada
        existing = Mahasiswa.query.filter_by(nim=nim).first()
        if existing:
            flash('NIM sudah digunakan mahasiswa lain.', 'error')
            return redirect(url_for('main.add_mahasiswa'))

        new_mhs = Mahasiswa(nama=nama, nim=nim, jurusan=jurusan)
        db.session.add(new_mhs)
        db.session.commit()
        flash("Mahasiswa berhasil ditambahkan.")
        return redirect(url_for('main.manage_mahasiswa'))

    return render_template('add_mahasiswa.html')

@main.route('/admin/mahasiswa/edit/<int:mhs_id>', methods=['GET', 'POST'])
@login_required
def edit_mahasiswa_form(mhs_id):
    if current_user.role.name != 'admin':
        return "Akses ditolak!", 403

    mhs = Mahasiswa.query.get_or_404(mhs_id)

    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']
        jurusan = request.form['jurusan']

        # Validasi duplikat NIM
        existing = Mahasiswa.query.filter_by(nim=nim).first()
        if existing and existing.id != mhs.id:
            flash('NIM sudah digunakan mahasiswa lain.', 'error')
            return redirect(url_for('main.edit_mahasiswa_form', mhs_id=mhs.id))

        mhs.nama = nama
        mhs.nim = nim
        mhs.jurusan = jurusan
        db.session.commit()
        flash("Data mahasiswa diperbarui.")
        return redirect(url_for('main.manage_mahasiswa'))

    return render_template('edit_mahasiswa.html', mhs=mhs)


@main.route('/admin/mahasiswa/delete/<int:mhs_id>', methods=['POST', 'GET'])
@login_required
def delete_mahasiswa(mhs_id):
    if current_user.role.name != 'admin':
        return "Akses ditolak!", 403

    from .models import Mahasiswa, db
    mhs = Mahasiswa.query.get_or_404(mhs_id)
    db.session.delete(mhs)
    db.session.commit()
    flash("Mahasiswa berhasil dihapus.")
    return redirect(url_for('main.manage_mahasiswa'))


@main.route('/mahasiswa/jadwal')
@login_required
def jadwal_mahasiswa():
    if current_user.role.name != 'mahasiswa':
        return "Akses ditolak!", 403

    mhs = Mahasiswa.query.filter_by(user_id=current_user.id).first()
    if not mhs:
        return "Data mahasiswa tidak ditemukan!", 404

    jadwals = Jadwal.query.filter_by(mahasiswa_id=mhs.id).all()
    return render_template('jadwal_mahasiswa.html', jadwals=jadwals)

@main.route('/dosen/jadwal')
@login_required
def jadwal_dosen():
    if current_user.role.name != 'dosen':
        return "Akses ditolak!", 403

    dosen = Dosen.query.filter_by(user_id=current_user.id).first()
    if not dosen:
        return "Data dosen tidak ditemukan!", 404

    jadwals = Jadwal.query.filter_by(dosen_id=dosen.id).all()
    return render_template('jadwal_dosen.html', jadwals=jadwals)

