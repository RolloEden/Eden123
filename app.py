from flask import Flask, redirect, url_for, render_template, request, flash, session
from werkzeug.utils import secure_filename
import datetime as dt
import shutil
import time
import os

main_directory = os.getcwd()

app = Flask(__name__)
app.secret_key = 'NFGPOESBHGPIUEARGBAWGRGPOUIREWA12321'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rbacixnjwdpcwz:ad7fcf3527b26121e9c9b980365804653b8dbabebdf8ccc506a05af6b32ad006@ec2-23-23-182-238.compute-1.amazonaws.com:5432/d3j05c7kls4f36'
app.config['UPLOAD_PATH'] = str(main_directory) + '\\static'


banned = False


banned_ips_list = []
file = open('bannedips.txt', 'r')
content = (str(file.read())).split('\n')
file.close()
for banned_ip in content:
    banned_ips_list.append(banned_ip)



@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        session['username']
        return redirect('/home')
    except:
        session['username'] = ''
        return redirect('/signin')



@app.route('/home', methods=['GET'])
def home():
    # checking ip
    try:
        session['username']
    except:
        return redirect('/')
    
    if session['username'] != '':
        # loading feed
        all_posts = []
        os.chdir(main_directory)
        os.chdir('POSTS')
        dir_ = os.getcwd()
        post_folders = os.listdir()
        print(post_folders)
        for post_folder in post_folders:

            # changing directories
            os.chdir(str(post_folder))

            # creating a sublist <=> to append it to the all_posts list
            sub_list = []

            # appending user's name to the sublist - 0
            users_name = ''
            for ch in post_folder:
                if not ch.isdigit():
                    users_name += ch
            sub_list.append(users_name)

            # appending the date - 1
            os.chdir(main_directory)
            os.chdir('POSTS')
            os.chdir(str(post_folder))
            file = open('date.txt', 'r')
            new_date = file.read()
            file.close()
            sub_list.append(str(new_date))

            # appending the profile picture - 2
            os.chdir(main_directory)
            os.chdir('static')
            files = os.listdir()
            for ext in ['.jpg', '.png', '.img']:
                if (str(users_name) + str(ext)) in files:
                    prof_pic = (str(users_name) + str(ext))
                else:
                    pass
            sub_list.append(prof_pic)

            # appending the title and description of the post to the sublist - 3
            os.chdir(main_directory)
            os.chdir('POSTS')
            os.chdir(str(post_folder))
            file = open('postitself.txt', 'r')
            content = file.read()
            file.close()
            content = content.split('\n')
            for s in content:
                sub_list.append(s)

            # appending the comments from the post to the sublist
            file = open('likes.txt', 'r')
            content = file.read()
            file.close()
            content = content.split('\n')
            sub_list.append(len(content))

            all_posts.append(sub_list)
            os.chdir(dir_)


        # loop's finished
        os.chdir(main_directory)
        all_posts.reverse()

        # all_posts = [ [username, pic, date, title, content, likes],      [username, pic, date, title, content, likes] ]
        #                      ^1Patrick                                            ^2David
        return render_template('home.html', posts=all_posts, logged_as=str(session['username']))
    else:
        return redirect('/signin')






        # CREATE A POST


@app.route('/create-post')
def create_post():
    try:
        # checking ip
        # ...
        if session['username'] != '':
            return render_template('create-post.html', logged_as=session['username'])
        else:
            return redirect('/signin')
    except:
        return redirect('/home')

@app.route('/checknewpost', methods=['POST', 'GET'])
def checknewpost():
        # checking ip
        # ...
        if session['username'] == '':
            return redirect('/signin')
        # redirecting user that arent logged in

        # changing directory

        os.chdir(main_directory)
        os.chdir('POSTS')
        all_file_names = os.listdir() 

        users_name = session['username']

        
        
        numbers_lst = []

        for file_name in all_file_names:
            number_chrs = ''
            for ch in file_name:
                if ch.isdigit() == True:
                    number_chrs += ch
            numbers_lst.append(int(number_chrs))
                

        last_highest_number = int(max(numbers_lst) + 1)


        users_file_name = str((int(last_highest_number))) + users_name


        os.chdir(main_directory)
        # changing directory
        os.chdir('POSTS')
        # creating the file
        os.mkdir(users_file_name)
        # joining a new path
        os.chdir(users_file_name)
        
        
    
        # creating the files inside the folder
        # creating 'postitself.txt' & 'like.txt' files
        new_file = open('postitself.txt', 'w')
        new_file.write(str(request.form['title']) + '\n' + str(request.form['content']))
        new_file.close()
        new_file2 = open('likes.txt', 'w')
        new_file2.close()

        # creating 'date.txt' file
        date = str((str(dt.date.today())).replace('-','.'))
        date = date.split('.')
        date.reverse()
        new_date = ''

        for el in date: 
            new_date += el + '.'
        file = open('date.txt', 'w')
        file.write(str(new_date[:-1]))
        file.close()
        return redirect('/home')



        # SIGN IN


@app.route('/signin')
def signin():

    # checking ip
    # ...
    return render_template('signin.html', redirected=False)


@app.route('/checksignin', methods=['GET', 'POST'])
def checksignin():
    # checking ip
    # ...

    os.chdir(main_directory)
    list_of_users = ((open('list of users.txt', 'r')).read()).split('\n')
    line_nr = 0
    real_password = ''
    for line in list_of_users:
        if request.form['username'] in line:
            real_password = (line.split(' '))[-1]


    if str(request.form['password']) == str(real_password):
        # logged in successfully
        #logged_file = open('logged.txt', 'w')
        os.chdir(main_directory)
        #logged_file.write(str(request.form['username']) + '\n' + str(request.form['password']))
        session['userdata'] = str(request.form['username']) + '\n' + str(request.form['password'])
        session['username'] = str(request.form['username'])
        #logged_file.close()
        #return '<h2>LOGGED IN SUCCESFULLY</h2>'
        return redirect('/home')
    else:
        #logged in unsuccessful
        return redirect('/signin')




        # SIGN UP
@app.route('/signup')
def signup():
    try:
        # checking ip
        ip_addr = request.remote_addr
        if ip_addr in banned_ips_list:
            session['username'] = ''
            return redirect('/home')
        else:
            pass
        return render_template('signup.html')
    except:
        return redirect('/signup')


@app.route('/checksignup', methods=['GET', 'POST'])
def checksignup():
    os.chdir(main_directory)
    file = open('list of users.txt', 'r')
    content = file.read()
    file.close()
    if request.form['username'] not in content and str(request.form['password']) == str(request.form['password2']):
        # adding the user on the "list of users" file
        file = open('list of users.txt', 'a')
        file.write('\n' + str(request.form['username']) + ' ' + str(request.form['password']))
        file.close()
        # creating a user's directory
        os.chdir(main_directory)
        os.chdir('Accounts')
        os.mkdir(str(request.form['username']))
        os.chdir(str(request.form['username']))
        file = open('bio.txt', 'w')
        file.write('')
        file.close()
        # create profile picture file (empty)
        os.chdir(main_directory)
        os.chdir('static')
        destination = str(os.getcwd() + '\\' + request.form['username'] + '.png')
        shutil.copyfile(os.getcwd() + '\\default.png', destination)
        file.close()
        return redirect('/home')
    else:
        return redirect('/signup')



        # LOG OUT

@app.route('/logout')
def logout():
    if session['username'] == '':
        return redirect('/signin')
    session['username'] = ''
    return redirect('/signin')



        # ACCOUNTS

@app.route('/<account>')
def Account(account):
    if session['username'] == '':
        return redirect('/signin')
    # getting the bio
    os.chdir(main_directory)
    os.chdir('Accounts')
    os.chdir(account)
    file = open('bio.txt', 'r')
    account_bio = file.read()
    file.close()
    # getting the profile picture
    os.chdir(main_directory)
    os.chdir('static')
    all_files = os.listdir()
    the_profile_picture = ''
    for ext in ['.jpg', '.png', '.img']:
        if (str(account) + str(ext)) in all_files:
            the_profile_picture = (str(account) + str(ext))
        else:
            pass
    # getting the posts posted by the user whos account is
    os.chdir(main_directory)
    os.chdir('POSTS')
    all_file_names = os.listdir()
    all_posts = []
    # START
    dir_ = os.getcwd()
    for post_folder in all_file_names:
        os.chdir(main_directory)
        os.chdir('POSTS')
        # changing directories
        os.chdir(str(post_folder))

        # creating a sublist <=> to append it to the all_posts list
        sub_list = []

        # appending user's name to the sublist
        users_name = ''
        for ch in post_folder:
            if not ch.isdigit():
                users_name += ch

        if users_name == account:
            sub_list.append(users_name)

            # appending the date
            os.chdir(main_directory)
            os.chdir('POSTS')
            os.chdir(str(post_folder))
            file = open('date.txt', 'r')
            new_date = file.read()
            file.close()
            sub_list.append(str(new_date))

            # appending the title and description of the post to the sublist
            os.chdir(main_directory)
            os.chdir('POSTS')
            os.chdir(str(post_folder))
            file = open('postitself.txt', 'r')
            content = file.read()
            file.close()
            content = content.split('\n')
            for s in content:
                sub_list.append(s)

            # appending the comments from the post to the sublist
            file = open('likes.txt', 'r')
            content = file.read()
            file.close()
            content = content.split('\n')
            sub_list.append(len(content))

            all_posts.append(sub_list)
            os.chdir(dir_)
        else:
            pass

    os.chdir(main_directory)
    all_posts.reverse()
    # FINISH
    if session['username'] == str(account):
        return render_template('account.html', acc=account, bio=account_bio, logged_as=session['username'], profile_picture=the_profile_picture, posts=all_posts, personal=True)
    else:
        return render_template('account.html', acc=account, bio=account_bio, logged_as=session['username'], profile_picture=the_profile_picture, posts=all_posts,  personal=False)







        # EDIT ACCOUNT
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if session['username'] == '':
        return redirect('/signin')
    return render_template('edit-account.html', logged_as=session['username'])


        # CONIFRM EDIT
@app.route('/comfirm_edit_bio', methods=['GET', 'POST'])
def confirm_edit_bio():
    usrname = str(session['username'])
    os.chdir(main_directory)
    os.chdir('Accounts')
    os.chdir(usrname.capitalize())
    
    file = open('bio.txt', 'w')
    file.write(request.form['new_bio'])
    file.close()
    return redirect(str('/' + str(session['username'])))


        # EDIT PROFILE IMAGE
@app.route('/editimage', methods=['POST', 'GET'])
def editimage():
    if request.method == 'POST':
        f = request.files['file_name']
        os.chdir(main_directory)
        os.chdir('static')
        the_file = ''
        for file in os.listdir():
            if session['username'] in file:
                the_file = file
        os.chdir(main_directory)
        os.chdir('static')
        os.remove(the_file)
        f.save(the_file)
        return redirect('/' + str(session['username']))
    return render_template('edit-image.html', logged_as=session['username'])


        # CHANGE PASSWORD
@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    # checking ip
    # ...
    os.chdir(main_directory)
    file = open('list of users.txt', 'r')
    content = file.read()
    file.close()
    if str(request.form['old_password']) in content and str(request.form['new_password']) == str(request.form['new_password2']):
        done = False
        users_new_line = ''
        after_ = ''
        before_ = ''
        for line in content.split('\n'):
            if str(session['username']) in line:
                users_new_line = (line.split(' '))[0] + ' ' + str(request.form['new_password'])
                done = True
            elif done:
                after_ += line + '\n'
            elif str(session['username']) in line:
                before_ += line + '\n'
        file = open('list of users.txt', 'w')
        file.write((before_ + '\n' + users_new_line + '\n' + after_).strip)
        file.close()
        return redirect('/' + str(session['username']))
    else:
        return redirect('/edit')


        # USERS
@app.route('/users')
def users():
    if session['username'] == '':
        return redirect('/signin')
    # all users list
    all_users = []
    file = open('list of users.txt', 'r')
    content = file.read()
    file.close()
    for user in content.split('\n'):
        all_users.append(user)
    return render_template('users.html', users=all_users, logged_as=session['username'])



        # CONTACT
@app.route('/contact')
def contact():
    return render_template('contact.html', logged_as=session['username'])


        # RULES
@app.route('/rules')
def rules():
    try:
        return render_template('rules.html', logged_as=session['username'])
    except:
        return redirect('/rules')

        # ABOUT US
@app.route('/aboutus')
def aboutus():
    if session['username'] == '':
        return redirect('/signin')
    return render_template('aboutus.html', logged_as=session['username'])


        # FORGOT PASSWORD
@app.route('/forgot-password')
def forgot_password():
    # checking ip
    ip_addr = request.remote_addr
    if ip_addr in banned_ips_list:
        session['username'] = ''
        return redirect('/home')
    return render_template('forgot_password.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
