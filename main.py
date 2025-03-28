from flask import Flask, request, jsonify, render_template, redirect
from sqlalchemy import desc
from settings import db, app
from models import User

#READ data from database & apply sorting, filtering, order_by
@app.route('/user/', methods=['GET', 'POST']) 
def get_all_users():
    print(">>>>> incoming query param ", request.args)
    if request.method == 'GET':
        try:
            # get method to retrieve all user data at list page using pagination
            order_by = request.args.get('order_by', None)
            page = request.args.get('page', 1, type=int)
            person_id = request.args.get('id') 
            keyword = request.args.get('name')
            email = request.args.get('email')
            password = request.args.get('password')
            mobile_number = request.args.get('mobile')
            #Search query --
            search_results = None
            if person_id:
                search_results = User.query.filter(User.id.startswith(person_id)).all()
            elif keyword:
                search_results = User.query.filter(User.name.startswith(keyword)).all()
            elif email:
                search_results = User.query.filter(User.email.contains(email)).all()
            elif password:
                search_results = User.query.filter(Usr.password.contains(password)).all()
            elif mobile_number:
                search_results = User.query.filter(User.mobile_number.contains(mobile_number)).all()
            #ordering --
            if order_by:
                if order_by[0] == "-":
                    order_by = order_by[1:]
                    pagination = User.query.order_by(desc(order_by.lower())).paginate(page=page, per_page=50, error_out=False)
                else:
                    pagination = User.query.order_by(order_by.lower()).paginate(page=page, per_page=50, error_out=False)
            else:
                pagination = User.query.paginate(page=page, per_page=50, error_out=False)

            current_user_Data = pagination.items
            print("Pagination items:", current_user_Data)

            return render_template('user.html', pagination=pagination, current_user_Data=current_user_Data, search_results=search_results)
        except:
                return  jsonify({"status": 500, "message": "Server error"})

    # POST method to create a new user
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        mobile_number = request.form['mobile_number']
        data = User(name=name,email=email, password=password, mobile_number=mobile_number)
        db.session.add(data)
        db.session.commit()
        return redirect('/user')

@app.route('/user/<int:id>', methods=['GET', 'POST'])
def retrieve_update_user(id):
    user = User.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('user_details.html', user=user)
    #UPDATE method to update a new user
    elif request.method == 'POST':  
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = request.form['password']
        user.mobile_number = request.form['mobile_number']            
        db.session.commit()
        return redirect('/user')
    else:
        return jsonify({"status": 500, "message": "HTTP method not allowed."})


@app.route('/user/<int:id>/delete', methods=['GET'])
def delete_user(id):
    if request.method == 'GET':
        try:
            user = User.query.filter_by(id=id).first()
            # return render_template('delete_user.html', user=user)
        except: 
            return jsonify({"status": 400, "message": "Given user not exists."})

        db.session.delete(user)
        db.session.commit()
        return redirect('/user')

    return jsonify({"status": 500, "message": "HTTP method not allowed."})

if __name__ == '__main__':
    db.create_all()
    app.run(host="0.0.0.0", port=5010, debug=True)
