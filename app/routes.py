from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

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
