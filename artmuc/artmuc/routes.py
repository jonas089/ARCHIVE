from artmuc.models import User, Post, db
from artmuc.forms import RegistrationForm, LoginForm, UpdateAccountForm, UpdateCustomerAccountForm , PostForm
from artmuc.mail import Mailer
from flask import render_template, request, redirect, session, url_for, flash, jsonify
from artmuc import app
from artmuc.evalid import validate_product_price, validate_artist_key
from flask_login import login_user, current_user, logout_user, login_required
import itsdangerous
import hashlib
import time
from PIL import Image
import os
import json

#Payment Gateway
import stripe

from wtforms.validators import ValidationError

stripe.api_key='sk_test_KoGkq0vUMMXep9fYOrOGWwR700oUIcU9JD'
stripe_pub = 'pk_test_20KQ2Vis1VY9ep6JnWeQxssn00NkW1agQW'

@app.route('/')
def home():
    return render_template('home.html', title='Home')

def load_accounts():
    accounts = User.query.all()
    return accounts

@app.route('/profiles')
def profiles():
    accounts = load_accounts()
    return render_template('profiles.html', accounts = accounts)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.artist_key.data:
            if validate_artist_key(form.artist_key.data) == False:
                flash(f'Artist Key Incorrect, Please Continue As A Customer Or Double Check', 'danger')
                return redirect('/registration')
        sha = hashlib.sha384()
        sha.update(form.password.data.encode('utf-8'))
        hashed_password = str(sha.hexdigest())
        user = User(username=form.username.data, email=form.email.data, artist_key=form.artist_key.data, password=hashed_password, verified="0")
        db.session.add(user)
        db.session.commit()
        Mailer(form.email.data, "Validate", token=itsdangerous.url_safe.URLSafeTimedSerializer('checkthoseemails').dumps(form.email.data))
        flash(f'Your Account Has Been Created! Please confirm your email! Double check your email and spam for confirmation!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Registration', form=form)

@app.route('/email_validation/<token>')
def email_validation(token):
    try:
        email = itsdangerous.url_safe.URLSafeTimedSerializer('checkthoseemails').loads(token, max_age=600)
        user = User.query.filter_by(email=email).first()
        user.verified = "1"
        #db.session.add(User(verified="1"))
        db.session.commit()
        return redirect(url_for('login'))
    except itsdangerous.exc.BadTimeSignature:
        return render_template('tokeninvalid.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        encoded_password = str(form.password.data).encode('utf-8')
        sha = hashlib.sha384()
        sha.update(encoded_password)
        hashed_password = str(sha.hexdigest())
        # User Validation
        if user and hashed_password == user.password:
            if user.verified == '1':
                login_user(user)
                return redirect('/account')
            Mailer(form.email.data, "Validate", token=itsdangerous.url_safe.URLSafeTimedSerializer('checkthoseemails').dumps(form.email.data))
            flash('Account unverified, email sent. Check your spam!')
        else:
            flash('Login Failed. Please Check Email And Password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

def save_picture(form_picture):
    sha = hashlib.sha256()
    f_ext = os.path.splitext(form_picture.filename)[1]
    sha.update((str(time.time()) + form_picture.filename).encode('utf-8'))
    generated_filename = str(sha.hexdigest()) + str(f_ext)
    picture_path = os.path.join(app.root_path, 'static/media/profile_pics', generated_filename)
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return generated_filename

@app.route('/delete/<product_picture_path>', methods=['GET'])
@login_required
def delete_product(product_picture_path):
    products = Post.query.all()
    owner = ''
    target = None
    for product in products:
        if product.product_picture_path == str(product_picture_path):
            owner = product.author.username
            target = product
    picture_path = os.path.join(app.root_path, 'static/media/products', target.product_picture_path)
    if target.is_sold != 'Yes':
        os.remove(picture_path)
    else:
        flash('You Are Not Allowed To Delete A Product That Has Been Sold', 'danger')
        return redirect('/account')
    if current_user.username != owner:
        flash('You Are Not Allowed To Change Data For This User [Error "validation"]', 'danger')
        return redirect('/account')
    else:
        db.session.delete(target)
        db.session.commit()
        return redirect('/')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if current_user.artist_key:
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.profile_picture_path = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.biography = form.biography.data
            db.session.commit()
            flash('Your Account Has Been Updated', 'success')
            return redirect('/account')
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
            form.biography.data = current_user.biography
        profile_picture_path = url_for('static', filename='media/profile_pics/' + current_user.profile_picture_path)
        products = Post.query.all()
        return render_template('account.html', title='account',
        profile_picture_path=profile_picture_path, form=form, products=products)
    else:
        form = UpdateCustomerAccountForm()
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.country = form.country.data
            current_user.address = form.address.data
            current_user.region = form.region.data
            current_user.zip = form.zip.data
            db.session.commit()
            flash('Your Account Has Been Updated', 'success')
            return redirect('/account')
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.country.data = current_user.country
            form.address.data = current_user.address
            form.region.data = current_user.region
            form.zip.data = current_user.zip
        profile_picture_path = url_for('static', filename='media/profile_pics/' + current_user.profile_picture_path)
        products = Post.query.all()
        return render_template('account.html', title='account',
        profile_picture_path=profile_picture_path, form=form, products=products)
def save_product_picture(form_picture):
    sha = hashlib.sha256()
    f_ext = os.path.splitext(form_picture.filename)[1]
    sha.update((str(time.time()) + form_picture.filename).encode('utf-8'))
    generated_filename = str(sha.hexdigest()) + str(f_ext)
    picture_path = os.path.join(app.root_path, 'static/media/products', generated_filename)
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return generated_filename

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    product_price_errors = []
    form = PostForm()
    if form.validate_on_submit():
        product_price_errors = validate_product_price(form.product_price.data)
        if form.picture.data and not product_price_errors:
            picture_file = save_product_picture(form.picture.data)
            post = Post(product_name = form.product_name.data, product_description = form.product_description.data, product_picture_path = picture_file, product_price = form.product_price.data, user_id = current_user.id, is_sold = 'No')
            db.session.add(post)
            db.session.commit()
            return redirect('/')
    return render_template('newpost.html', title='Add A Product', form=form, product_price_errors=product_price_errors)

@app.route('/gallery/<artist>', methods=['GET'])
def visit_artist(artist):
    artist_data = User.query.filter_by(username=artist).first()
    products = Post.query.all()
    return render_template('gallery.html', title='Gallery', author=artist, products=products, artist_data=artist_data, key=stripe_pub)


def get_product(product_id):
    products = Post.query.all()
    for product in products:
        if product.id == product_id:
            return product
    return False

@app.route('/product/<id>', methods=['GET'])
@login_required
def view_product(id):
    product = get_product(int(id))
    return render_template('product.html', product=product, key=stripe_pub)

@app.route('/charge', methods=['POST', 'GET'])
@login_required
def charge():
    response = jsonify('error')
    response.status_code = 500
    product = get_product(int(request.json['product']))

    purchased_product_data = {
    'product_id' : product.id,
    'product_name' : product.product_name,
    'product_description' : product.product_description,
    'product_price' : product.product_price,
    'product_author_username' : product.author.username,
    'product_author_email' : product.author.email
    }

    if product:
        users = User.query.all()
        try:
            product = get_product(int(request.json['product']))
            customer = stripe.Customer.create(
                email=current_user.email,
                source=request.json['token']
            )

            # This Works Fine // Charges Card And Pays To Stripe Account
            stripe.Charge.create(
                customer=customer.id,
                amount=int(product.product_price * 100),
                currency='eur',
                application_fee_amount=int(product.product_price * 100 * 0.05), # 5% platform fee
                transfer_data={
                'destination': product.author.stripe_account_id
                }
            )
            response = jsonify('success')
            response.status_code = 202
            product.is_sold = 'Yes'

            ###############################
            #  DEBUG CAREFULLY            #
            ###############################
            product.customer_email = current_user.email
            product.customer_country = current_user.country
            product.customer_region = current_user.region
            product.customer_address = current_user.address
            product.customer_zip = current_user.zip
            db.session.commit()
            # SEND PAYMENT CONFIRMATION MAILS HERE

        except stripe.error.StripeError:
            return response
    return response

@app.route('/stripe_checkout', methods=['GET', 'POST'])
@login_required
def stripe_checkout():
    auth_token = request.args.get('code')
    try:
        response = stripe.OAuth.token(
        grant_type='authorization_code',
        code=auth_token
        )
        current_user.stripe_account_id = response['stripe_user_id']
        db.session.commit()
        flash("You'r Payment Method Has Been Added, You Can Now Receive Payments!", 'success')
    except Exception as Checkout_Error:
        flash('Checkout Failed, Payment Method Not Active!', 'danger')

    return redirect('/account')

@app.route('/balances', methods=['GET'])
@login_required
def balances():
    stripe_balance = stripe.Balance.retrieve(stripe_account=current_user.stripe_account_id)
    pending_balance = stripe_balance['pending'][0]['amount']
    available_balance = stripe_balance['available'][0]['amount']
    stripe_balance_data = {'available' : available_balance, 'pending' : pending_balance}
    products = Post.query.all()
    if not current_user.artist_key:
        return redirect('/account')
        flash("You Don't Have Permission To View Artist-Panels", 'danger')
    return render_template('balances.html', artist_data=current_user, products=products, stripe_balance_data = stripe_balance_data)

#id = db.Column(db.Integer, primary_key=True)
#product_name = db.Column(db.String(25), nullable=False)
#product_description = db.Column(db.String(250), nullable=False)
#product_picture_path = db.Column(db.String(260), nullable=False)
#product_price = db.Column(db.Float, nullable=False)
#user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#is_sold = db.Column(db.Integer, nullable=False)
