import psycopg2
import requests
from flask import *
from flask_login import login_user, logout_user, login_required, current_user
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
# from readGrades import readGrades


auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        # generate_password_hash(request.form.get("password"), method='sha256')
        user_type = request.form.get("user_type")
        # generate_password_hash()
        new_user = Users(login=request.form.get("login"),
                     password=generate_password_hash(request.form.get("password")),
                     user_type=user_type,
                     email=request.form.get("email"),
                     phone_nr=request.form.get("phone_nr"),
                     photo=f'{request.form.get("login")}.jpg',
                     logged_in=False)
        db.session.add(new_user)
        db.session.commit()

        user_id = new_user.user_id
        if user_type == "student":
            new_student = Students(student_id=user_id,
                                   name=request.form.get("name"),
                                   surname=request.form.get("surname"),
                                   gradebook_nr=request.form.get("gradebook_nr"),
                                   class_name=request.form.get("class_name"),
                                   date_of_birth=request.form.get("date_of_birth"),
                                   place_of_birth=request.form.get("place_of_birth"),
                                   address=request.form.get("address"))
            db.session.add(new_student)

        elif user_type == "parent":
            new_parent = Parents(parent_id=user_id,
                                 name=request.form.get("name"),
                                 surname=request.form.get("surname"),
                                 student_id=request.form.get("student_id"))
            db.session.add(new_parent)
        elif user_type == "teacher":
            new_teacher = Teachers(teacher_id=user_id,
                                   name=request.form.get("name"),
                                   surname=request.form.get("surname"),
                                   classroom_nr=request.form.get("classroom_nr"),
                                   description=request.form.get("description"))
            db.session.add(new_teacher)

        db.session.commit()

        flash('Account created!', category='success')
        return redirect(url_for('views.profile'))
    return render_template("sign_up.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            login=request.form.get("username")).first()
        if user.password == request.form.get("password"):
        # if check_password_hash(user.password, request.form.get("password")):
            login_user(user, remember=True)
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            session['user_type'] = user.user_type
            session['email'] = user.email
            session['phone'] = user.phone_nr

            flash('Logged in!', category='success')

            if user.user_type == 'teacher':
                teacher = Teachers.query.filter_by(teacher_id=user.user_id).first()
                session['name'] = teacher.name
                session['surname'] = teacher.surname
                session['classroom_nr'] = teacher.classroom_nr
                session['description'] = teacher.description

            if user.user_type == 'parent':
                parent = Parents.query.filter_by(parent_id=user.user_id).first()
                session['parent_id'] = parent.parent_id
                session['name'] = parent.name
                session['surname'] = parent.surname

                session['child_id'] = parent.student_id
                child = Students.query.filter_by(student_id=parent.student_id).first()
                session['child_name'] = child.name
                session['child_surname'] = child.surname
                session['child_gradebook_nr'] = child.gradebook_nr
                session['child_class_name'] = child.class_name
                session['child_date_of_birth'] = child.date_of_birth
                session['child_place_of_birth'] = child.place_of_birth
                session['child_address'] = child.address

            if user.user_type == 'student':
                student = Students.query.filter_by(student_id=user.user_id).first()
                session['student_id'] = student.student_id
                session['name'] = student.name
                session['surname'] = student.surname
                session['gradebook_nr'] = student.gradebook_nr
                session['class_name'] = student.class_name
                date = student.date_of_birth
                session['date_of_birth'] = date.strftime("%d %B %Y")
                session['place_of_birth'] = student.place_of_birth
                session['address'] = student.address

            if user.user_type != 'teacher':

                if user.user_type == 'student':
                    id_for_grades = user.user_id
                else:
                    id_for_grades = parent.student_id

                # session['mat_grades'], session['bio_grades'], session['che_grades'], session['phi_grades'], session[
                #     'mat_ave'], session['bio_ave'], session['che_ave'], session['phi_ave'] = readGrades(id_for_grades)
                con = psycopg2.connect(database="dziennik_baza",
                                       user="dziennik_baza_user",
                                       password="MNCZoIpG5hmgoEOHbGfvd15c5Br7KZfc",
                                       host="dpg-cldiadbmot1c73dot240-a.frankfurt-postgres.render.com",
                                       port="5432")
                cur = con.cursor()
                cur.execute("SELECT g.type, s.subject_name FROM grades g JOIN subjects s ON g.subject_id=s.subject_id AND g.student_id = %(id)s", {'id': id_for_grades})
                grades_data = cur.fetchall()
                cur.close()
                con.close()

                mat = list()
                bio = list()
                che = list()
                phi = list()
                for row in grades_data:
                    if row[1] == 'matematyka':
                        mat.append(row[0])
                    if row[1] == 'biologia':
                        bio.append(row[0])
                    if row[1] == 'chemia':
                        che.append(row[0])
                    if row[1] == 'fizyka':
                        phi.append(row[0])
                session['mat_grades'] = mat
                session['bio_grades'] = bio
                session['che_grades'] = che
                session['phi_grades'] = phi
                if len(mat) != 0:
                    session['mat_ave'] = sum(mat) / len(mat)
                else:
                    session['mat_ave'] = '-'

                if len(bio) != 0:
                    session['bio_ave'] = sum(bio)/len(bio)
                else:
                    session['bio_ave'] = '-'

                if len(che) != 0:
                    session['che_ave'] = sum(che)/len(che)
                else:
                    session['che_ave'] = '-'

                if len(phi) != 0:
                    session['phi_ave'] = sum(phi)/len(phi)
                else:
                    session['phi_ave'] = '-'

            return redirect(url_for("views.profile"))
    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
