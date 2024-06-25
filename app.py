from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:2001Alina@localhost/FitnessCenterDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

class WorkoutSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    member = db.relationship('Member', backref=db.backref('workout_sessions', lazy=True))

class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member

class WorkoutSessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutSession

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

@app.route('/')
def home():
    return 'Hello, this is the home page!'

@app.route('/members', methods=['POST'])
def add_member():
    name = request.json['name']
    email = request.json['email']
    age = request.json['age']
    new_member = Member(name=name, email=email, age=age)
    db.session.add(new_member)
    db.session.commit()
    return member_schema.jsonify(new_member)

@app.route('/members', methods=['GET'])
def get_members():
    all_members = Member.query.all()
    result = members_schema.dump(all_members)
    return jsonify(result)

@app.route('/members/<id>', methods=['GET'])
def get_member(id):
    member = Member.query.get(id)
    return member_schema.jsonify(member)

@app.route('/members/<id>', methods=['PUT'])
def update_member(id):
    member = Member.query.get(id)
    name = request.json['name']
    email = request.json['email']
    age = request.json['age']
    member.name = name
    member.email = email
    member.age = age
    db.session.commit()
    return member_schema.jsonify(member)

@app.route('/members/<id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get(id)
    db.session.delete(member)
    db.session.commit()
    return member_schema.jsonify(member)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
