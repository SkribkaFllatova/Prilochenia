from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User

app = Flask(__name__) #Создаем экземпляр приложения Flask.
app.secret_key = "123" #Устанавливаем секретный ключ для приложения, который используется для защиты сессий и других данных.

user_db = "skribkafilatova"
host_ip ="127.0.0.1"
host_port = "5432"
database_name = "lab5"
password = "1234"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://skribkafilatova:postgres@localhost/lab5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных и менеджера авторизации
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Эндпоинт для корневой страницы
@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', name=current_user.name)
    else:
        return redirect(url_for('login'))

# Эндпоинт для страницы входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Проверка заполнения полей
        if not email or not password:
            flash("Заполните все поля", "error")
            return redirect(url_for('login'))

        # Поиск пользователя по email
        user = User.get_by_email(email)
        if not user:
            flash("Данный пользователь не найден", "error")
            return redirect(url_for('login'))

        # Проверка пароля
        if not user.check_password(password):
            flash("Введен неверный пароль", "error")
            return redirect(url_for('login'))

        # Авторизация пользователя
        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html')

# Эндпоинт для страницы регистрации
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Проверка заполнения полей
        if not name or not email or not password:
            flash("Заполните все поля", "error")
            return redirect(url_for('signup'))

        # Проверка на существование пользователя
        if User.get_by_email(email):
            flash("Пользователь с таким email уже существует", "error")
            return redirect(url_for('signup'))

        # Создание нового пользователя
        new_user = User(name=name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Регистрация прошла успешна! Войдите, используя свои данные.")
        return redirect(url_for('login'))

    return render_template('singup.html')

# Эндпоинт для выхода
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создаёт таблицы в базе данных при первом запуске
    app.run(debug=True)
