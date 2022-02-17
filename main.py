from flask_login import current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
import uuid
from datetime import datetime


from itsdangerous import json
from .models import Contest, Proposal
import os
from . import db

main = Blueprint('main', __name__)
path_root = os.path.abspath(os.curdir)



@main.route('/home')#FuncionaBIEN
def home():
    
    table = []
    
    for doc in Contest.query.all():
        table.append({
            'id_contest'   : doc.id_contest, 
            'id_user'      : doc.id_user, 
            'contest_name' : doc.contest_name,   
            'banner_name'  : doc.banner_name,  
            'url_contest'  : doc.url_contest, 
            'start_date'   : doc.start_date, 
            'end_date'     : doc.end_date,  
            'award'        : doc.award,   
            'dialog'       : doc.dialog,   
            'desciption'   : doc.desciption 
        }

        )
    return jsonify(table)

@main.route('/delete_contest/<id>', methods=['DELETE'])#FuncionaBien
def delete_contest(id):  
    Contest.query.filter_by(id_contest=id).delete()
    db.session.commit()
    flash('Evento eliminado.')
    table = []
    for doc in Contest.query.all():
        table.append({
            'id_contest'   : doc.id_contest, 
            'id_user'      : doc.id_user, 
            'contest_name' : doc.contest_name,   
            'banner_name'  : doc.banner_name,  
            'url_contest'  : doc.url_contest, 
            'start_date'   : doc.start_date, 
            'end_date'     : doc.end_date,  
            'award'        : doc.award,   
            'dialog'       : doc.dialog,   
            'desciption'   : doc.desciption 
        }

        )
    return jsonify(table)

@main.route('/view_contest/<id>')#Funciona BIEN
def view_contest(id):
    query = Contest.query.filter_by(id_contest=id).first()
    return jsonify({
            'id_contest'   : query.id_contest, 
            'id_user'      : query.id_user, 
            'contest_name' : query.contest_name,   
            'banner_name'  : query.banner_name,  
            'url_contest'  : query.url_contest, 
            'start_date'   : query.start_date, 
            'end_date'     : query.end_date,  
            'award'        : query.award,   
            'dialog'       : query.dialog,   
            'desciption'   : query.desciption })


@main.route('/edit_contest/<id>', methods=['PUT'])#Corregir porque no Actualiza
def edit_contest(id):
  
    dict = request.json
    #if dict['start_date']!='':
    #    dict['start_date'] = datetime.strptime(dict['start_date'],"%Y-%m-%d")
    #if dict['end_date'] !='':
    #    dict['end_date'] = datetime.strptime(dict['end_date'],"%Y-%m-%d")
    dict_filter = {k: v for k, v in dict.items() if len(str(v)) != 0}
    
    Contest.query.filter(Contest.id_contest == id).update(dict_filter)
    query = Contest.query.filter_by(id_contest=id).first()
    return jsonify({
            'id_contest'   : query.id_contest, 
            'id_user'      : query.id_user, 
            'contest_name' : query.contest_name,   
            'banner_name'  : query.banner_name,  
            'url_contest'  : query.url_contest, 
            'start_date'   : query.start_date, 
            'end_date'     : query.end_date,  
            'award'        : query.award,   
            'dialog'       : query.dialog,   
            'desciption'   : query.desciption })

@main.route('/create_contest_post/', methods=['POST'])#Sirve, pero se debe arreglar Id debe ser la del current_user
def create_contest_post(): 
    contest_name = request.json["name"]
    #start_date = request.json.get('datestart')
    #end_date = request.json.get('dateend')
    award = int(request.json.get('award'))
    dialog = request.json.get('dialog')
    description = request.json.get('description')
    query = Contest.query.filter_by(id_contest=3).first()
    #banner = request.files['file']

    #filename = str(uuid.uuid1()) + '.' + banner.filename.split('.')[-1]
    #banner.save( path_root+ '/proyecto_01/static/uploads/images' + filename)
    new_contest = Contest(id_user =15, #current_user.id,
                          contest_name = contest_name,
                          banner_name='/prueba.jpeg',#filename,
                          url_contest='192.168.0.1:8080/abcd',
                          start_date=query.start_date,#datetime.strptime(str(start_date),"%Y-%m-%d"),
                          end_date= query.start_date,#datetime.strptime(str(end_date),"%Y-%m-%d"),
                          award=12,
                          dialog=dialog,
                          desciption=description)
    db.session.add(new_contest)
    db.session.commit()
    query = Contest.query.filter_by(contest_name=contest_name).first()
    return jsonify({
            'id_contest'   : query.id_contest, 
            'id_user'      : query.id_user, 
            'contest_name' : query.contest_name,   
            'banner_name'  : query.banner_name,  
            'url_contest'  : query.url_contest, 
            'start_date'   : query.start_date, 
            'end_date'     : query.end_date,  
            'award'        : query.award,   
            'dialog'       : query.dialog,   
            'desciption'   : query.desciption})

@main.route('/apply/<id>')#SirveBien
def apply(id):
    query = Contest.query.filter_by(id_contest=id).first()
    return jsonify({
            'id_contest'   : query.id_contest, 
            'id_user'      : query.id_user, 
            'contest_name' : query.contest_name,   
            'banner_name'  : query.banner_name,  
            'url_contest'  : query.url_contest, 
            'start_date'   : query.start_date, 
            'end_date'     : query.end_date,  
            'award'        : query.award,   
            'dialog'       : query.dialog,   
            'desciption'   : query.desciption })

@main.route('/apply', methods=['POST'])
def applied_post():
    id_contest = request.json.get('idContent')
    email = request.json.get('emailLocutor')
    query_user = Proposal.query.filter_by(id_contest=id_contest,email=email).first()

    if query_user is not None:
        resultado='el usuario ya aplicó a este evento'

    song = request.files['file']

    if len(song.filename)==0:
        resultado='el usuario debe adjuntar un audio'

    proposal_formato = song.filename.split('.')[-1]
    song_filename = str(uuid.uuid1()) + '.' + song.filename.split('.')[-1]
    if proposal_formato == 'mp3':
        song.save(path_root + '/proyecto_01/static/uploads/dialog_song_convert/' + song_filename)
        state_voice = 'convert'
        dialogo_sound_convert = song_filename
    else:
        song.save(path_root + '/proyecto_01/static/uploads/dialog_song/' + song_filename)
        state_voice = 'in process'
        dialogo_sound_convert = None
    new_proposal = Proposal(id_contest = int(id_contest),
                            create_date= datetime.now(),
                            full_name_speaker = request.json.get('nombreLocutor'),
                            email= email,
                            dialogo_sound= song_filename,
                            dialogo_sound_convert= dialogo_sound_convert,
                            formato=proposal_formato,
                            state_voice=state_voice,
                            observacion=request.json.get('observacionLocutor'))
    db.session.add(new_proposal)
    db.session.commit()
    return resultado







