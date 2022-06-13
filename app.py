import time

# motor
import RPi.GPIO as GPIO
import flask
from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, LoginManager
from flask_login import login_required
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

GPIO.setmode(GPIO.BOARD)

from .models import db, Users, Recipe, Coops
from .schema import RecipeSchema, CoopsSchema, ma

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///easymixdb.sqlite'
app.config['SECRET_KEY'] = 'x.@&F{jW3*}$8&pN+p#ot>n&QS$?'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
ma.init_app(app)
# setting flask login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '.login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/')
def easyindex():
    return render_template('index.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html',
                           username=current_user.username, id=current_user.id, phone=current_user.phone,
                           email=current_user.email
                           )


@app.route('/updatemyprofile')
@login_required
def updprofile():
    return render_template('updatemyprofile.html'
                           )


@app.route('/myprofile/update/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_myprofile(id):
    # form = User
    # form = UserForm
    if request.method == "POST":
        name_to_update = Users.query.get_or_404('id')

        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['phone']
        # UPDATE PASSWORD

        db.session.commit()
        flash("User updated successfully")
        # return redirect("updatemyprofile.html")
        return redirect(url_for('updatemyprofile'))


@app.route('/displaycoop')
@login_required
def display_coop():
    return render_template('displaycoop.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Users.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))  # if the user doesn't exist or password is wrong, reload the page
    login_user(user, remember=remember)
    return redirect('/farmer_dashboard')


@app.route('/add_coop')
@login_required
def add_coop():
    return render_template('add_coop.html')


@app.route('/Easymix_previewmycoop')
@login_required
def preview_coop():
    return render_template('Easymix_previewmycoop.html')


@app.route('/Easymix_viewmycoop')
@login_required
def viewmycoop():
    return render_template('Easymix_viewmycoop.html')


@app.route('/coop_adding', methods=['POST', 'GET'])
def addcoop_post():
    # id  --> auto
    # name  --> supplied
    # age --> supplied
    # breed  --> supplied
    # number_of_days_to_feed --> supplied, in a range
    # number_of_chicks  --> supplied
    # date_for_next_feed --> auto
    # date_added --> auto
    # user_id --> auto
    # recipe_object  --> auto

    name = request.form.get('name')
    # TODO : the farmer can only input numbers
    age = int(request.form.get('age'))
    breed = request.form.get('breed')
    number_of_chickens = int(request.form.get('number_of_chickens'))
    new_coop = Coops(name=name, breed=breed, age=age, number_of_chickens=number_of_chickens, user_id=current_user.id)
    db.session.add(new_coop)
    db.session.commit()
    flash('Coop added successfully')
    return redirect('/coop/add_days_to_feed/' + str(new_coop.id))


@app.route('/coop/add_days_to_feed/<int:id>', methods=['GET', 'POST'])
#def add_days_coops(id_):
def add_days_coops(id):    
    # id  --> auto
    # name  --> supplied
    # age --> supplied
    # breed  --> supplied
    # number_of_days_to_feed --> supplied, in a range
    # number_of_chicks  --> supplied
    # date_for_next_feed --> auto
    # date_added --> auto
    # user_id --> auto
    # recipe_object  --> auto
    
    coop_instance = Coops.query.filter_by(id=id).one_or_none()
    # logic to calculate available number of days to feed
    available_days = 0
    
    
    #logic to calculate current age
    if coop_instance.breed == "layers":

        if coop_instance.age >= 0 <= 28:
            "chick mash"
            available_days = 28 - coop_instance.age

        elif coop_instance.ageage > 28 <= 119:
            "growers mash"
            available_days = 119 - coop_instance.age
        else:
            "layers mash"
            available_days = 200

    # get the available days for adding feed
    if flask.request.method == 'GET':

        return render_template('number_of_days_to_feed.html', data={"available_days": available_days})


    else:
        # validate if entered days are valid
        number_of_days_to_feed = int(request.form.get('number_of_days_to_feed'))
        if available_days == 200:
            # we dont need to validate what the farmer entered
            pass
        else:
            if available_days < number_of_days_to_feed:
                # this is an error, the farmer has entered wrong value
                flash('Please enter correct data')
                return redirect('/coop/add_days_to_feed/' + str(coop_instance.id))


#     # the logic of calculating days for next feed & feed type
#     if breed == "layers":
#         feed = ""
#         wmaize = 0
#         soya = 0
#         fishm = 0
#         maizeb = 0
#         limes = 0
           # wheat = 0
           # gnut = 0

#         multiply_by = number_of_days_to_feed * number_of_chickens * daily_consumption


#         if age >= 0 <= 28:
#             "chick mash"
#             daily_consumption = 110
#             wmaize = (0.5 * multiply_by)
#             soya = (0.2 * multiply_by)
#             fishm = (0.1 * multiply_by)
#             maizeb = (0.1 * multiply_by)
#             limes = (0.1 * multiply_by)
#             result = wmaize + soya + fishm + maizeb + limes
#             feed = "chick mash"
#
#
#
#         elif age > 28 <= 119:
#            "growers mash"
#             daily_consumption = 150
#             wmaize = (0.5 * multiply_by)
#             soya = (0.2 * multiply_by)
#             wheat = (0.3 * multiply_by)
#             result = wmaize + soya + wheat
#             feed = "growers mash"
#
#         else:
#             "layers mash"
#             daily_consumption = 150
#             wmaize = (0.3 * multiply_by)
#             fishm= (0.2 * multiply_by)
#             wheat = (0.3 * multiply_by)
#             gnut = (0.2 * multiply_by)
#             result = wmaize + wheat + fishm +gnut
#             feed = "layers mash"
#
#         print(result)
#         # saving the results into database
#         recipe_instance = Recipe(feed=feed, number_of_days_to_feed=" ", result=result, user_id=current_user.id)
#         db.session.add(recipe_instance)
#         db.session.commit()
#
#     # push to database
#
#
# #     coop = Coops.query.filter_by(
# #         name=name).first()
# #
# #     if coop:
# #         flash('The chicken house with this name already exists')
# #         return redirect('/farmer_dashboard')


@app.route('/coops/show', methods=['POST', 'GET'])
def get_coop_data():
    coop_schema = CoopsSchema(many=True)

    all_coops = Coops.query.filter_by(user_id=current_user.id).all()
    coop_data = coop_schema.dump(all_coops)

    return render_template(
        'displaycoop.html',
        data=coop_data
    )


@app.route('/mypreview', methods=['POST', 'GET'])
def get_mypreviewcoop_data():
    previewcoop_schema = CoopsSchema(many=True)

    preview_coop = Coops.query.filter_by(user_id=current_user.id).all()
    mycoop_preview = previewcoop_schema.dump(preview_coop)

    return render_template(
        'Easymix_previewmycoop.html',
        data=mycoop_preview
    )


# @app.route('/viewmycoop', methods=['POST', 'GET'])
# def get_viewmycoop_data():
#     viewcoop_schema = CoopsSchema(many=True)
#
#     #     view_coop = Coops.query.filter_by(user_id=current_user.id).all()
#     #     mycoop_view = previewcoop_schema.dump(preview_coop)
#
#     # Need to view only that specific coop for my current user ID ---KOndwani
#     # then have calculate and cancel option
#
#     return render_template(
#         'Easymix_viewmycoop.html',
#         data=mycoop_view
#     )


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    phone = request.form.get('phone')
    user = Users.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect('/signup')

    # creating a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = Users(email=email, phone=phone, username=name,
                     password=generate_password_hash(password, method='sha256'))
    flash('You have been added succesfully')
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect('/login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/layers')
@login_required
def layers():
    return render_template('layers.html')


@app.route('/layers_all')
@login_required
def layersall():
    return render_template('layers_all.html')


# @app.route('/admin_dashboard')
# @login_required
# def admin_db():
#     id = current_user.id
#     if id == :
#         return render_template('admin_dashboard.html')
#     else:
#         flash("sorry you must be Admin to access this page")
#         return redirect(url_for('login'))
#     

@app.route('/farmer_dashboard')
@login_required
def farmer_db():
    return render_template('farmer_dashboard.html', username=current_user.username)


@app.route('/admin_dashboard')
def admin_db():
    return render_template('/admin_dashboard.html')


  
# @app.route('/calc_result', methods=['POST', 'GET'])
# @login_required
# def calc_result():  # ~ Route to send calculator form input
    # error = ''
    # result = ''
    # wmaize = ''
    # soya = ''
    # fishm = ''
    # maizeb = ''
    # limes = ''

    # amount_input = request.form['total']
    # feed = request.form['feed']
    # input1 = float(amount_input)

    # if feed == "layers1":
        # wmaize = (0.5 * input1)
        # soya = (0.2 * input1)
        # fishm = (0.1 * input1)
        # maizeb = (0.1 * input1)
        # limes = (0.10 * input1)
        # result = wmaize + soya + fishm + maizeb + limes
        # print(result)
        # # saving the results into database
        # recipe_instance = Recipe(feed=feed, amount_entered=amount_input, result=result, user_id=current_user.id)
        # db.session.add(recipe_instance)
        # db.session.commit()

        # return render_template(
            # 'layers1.html',
            # input1=input1, feed=feed,
            # wmaize=wmaize,
            # soya=soya,
            # maizeb=maizeb,
            # fishm=fishm,
            # limes=limes,
            # result=result)


@app.route('/demo')
def demo():
    return render_template('demo.html')


@app.route('/demo_calc', methods=['POST', 'GET'])
def demo_calc():
    ufa = ''  # feed A
    soya = ''  # feed B

    amount_input = request.form['total']
    feed = request.form['feed']
    input1 = float(amount_input)
    if feed == "demo":
        ufa = (
                0.5 * input1)  # ufa,soya,fishmeal answer will be stored in db, create a demo db with fields for these three
        soya = (0.3 * input1)
        # fishmeal = (0.2*input1)

    motor1 = [7, 11, 13, 15]  # first motor pins defined
    motor2 = [29, 31, 33, 35]

    # for motor 1 ufa
    for pin in motor1:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
    halfstep_seq = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1]
    ]

    for i in range(int(512 * ufa)):  # rotating for feed A
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(motor1[pin], halfstep_seq[halfstep][pin])
                time.sleep(0.001)
    # GPIO.cleanup()

    # for motor 1 end

    # motor 2
    for pin in motor2:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    for i in range(int(512 * soya)):  # rotating for feed A
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(motor2[pin], halfstep_seq[halfstep][pin])
                time.sleep(0.001)
    GPIO.cleanup()

    # motor2 end

    return render_template(
        'demo_result.html',
        input1=input1, feed=feed,
        ufa=ufa, soya=soya)


@app.route('/user/results', methods=['POST', 'GET'])
@login_required
def get_past_calc_result():
    recipe_schema = RecipeSchema(many=True)

    all_users_recipe = Recipe.query.filter_by(user_id=current_user.id).all()
    recipe_data = recipe_schema.dump(all_users_recipe)

    return render_template(
        'layers_all.html',
        data=recipe_data
    )


def create_app():
    db.init_app(app)
    Migrate(app, db)
    return app


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
