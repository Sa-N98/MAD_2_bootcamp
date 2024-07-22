from flask_restful import Resource,reqparse
from model import *
import json
from flask_jwt_extended import jwt_required



class search(Resource):
    @jwt_required()
    def get(self,tags, search_query):

        if tags == 'Song':
            results = songs.query.filter(songs.name.like('%'+search_query+'%')).all()
           
        elif tags == 'Artist':
            results = songs.query.filter(songs.artist.like('%'+search_query+'%')).all()
           
        elif tags == 'Album':
            results = songs.query.filter(songs.album.like('%'+search_query+'%')).all()
        


        data = {}
        count=1
        for item in results:
            data['song'+str(count)]=[item.name, item.url]
            count+=1
            
        
        json_data = json.dumps(data)
        return  json_data
        