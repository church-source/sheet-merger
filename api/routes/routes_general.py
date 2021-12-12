#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask import current_app as app

import re
import requests
import json
import time
import PyPDF2
from flask import make_response
from flask import send_file
import io

route_path_general = Blueprint("route_path_general", __name__)
codeRegex = re.compile('^[A-z]{1,5}[0-9]*$', re.I)
sheetTypeRegex = re.compile('^(guitar|piano|lyrics|lead)*$', re.I)
#token_cache = {}

@route_path_general.route('/songbook/<string:sheet_type>', methods=['GET'])
def get_sheet(sheet_type):
    if bool(sheetTypeRegex.match(str(sheet_type))) == False:
        return "Invalid Book Type", 400
    else:

        codes = request.args.getlist('code')
        friendly = request.args.get("friendly")
        two_page_friendly = True
        if friendly == 'false':
            two_page_friendly = False

        reload = request.args.get("reload")
        force_reload = False
        if reload == 'true':
            force_reload = True

        merge_file = PyPDF2.PdfFileMerger(strict=False)
        pdf_merged_buffer = io.BytesIO()

        total_pages = 0
        current_sheet = 0

        sheet_name = sheet_type+"book_"
        for code in codes:
            if bool(codeRegex.match(str(code))) == False:
                return "Invalid Song Code", 400
            sheet_name = sheet_name + code
        if two_page_friendly:
            sheet_name = sheet_name + "_friendly"


        if force_reload is False:
            try:
                existing_pdf = open(app.config['SONGBOOK_TMP_DIR'] + sheet_name + ".pdf", 'rb')
                if existing_pdf is not None:
                    return send_file(app.config['SONGBOOK_TMP_DIR'] + sheet_name + ".pdf",
                                     attachment_filename=sheet_name + ".pdf")
            except Exception as e:
                print(e)
                # do nothing
                print("error trying to read from songbook cache")

        token = authorize_and_get_token()
        for code in codes:
            if bool(codeRegex.match(str(code))) == False:
                return "Invalid Song Code", 400

            pdfdoc_remote = get_pdf_for_code(code, sheet_type, token)
            merge_file.append(pdfdoc_remote)
            total_pages += pdfdoc_remote.numPages
            if two_page_friendly and (total_pages % 2 != 0 and current_sheet != (len(codes)-1)):
                # current sheet starts at 1. so
                len_of_next_sheet = get_pdf_for_code(codes[current_sheet+1], sheet_type, token).numPages
                if len_of_next_sheet != 1:
                    blank_pdf = PyPDF2.PdfFileReader("blank.pdf")
                    if blank_pdf:
                        merge_file.append(blank_pdf)
                        print ('adding blank page')
                        total_pages += 1

            current_sheet += 1
            print(pdfdoc_remote.numPages)

        result_pdf = open('./temp/' + sheet_name + ".pdf", 'wb')
        merge_file.write(result_pdf)
        result_pdf.close()

        merge_file.write(pdf_merged_buffer)
        response = make_response(pdf_merged_buffer.getvalue())

        # Set headers so web-browser knows to render results as PDF
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['mimetype'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            'filename=%s.pdf' % sheet_name
        return response


def get_pdf_for_code(code, sheet_type, token):
    response = get_song_from_song_api(sheet_type, code, token)
    response_bytes = io.BytesIO(response.content)
    pdfdoc_remote = PyPDF2.PdfFileReader(response_bytes)
    return pdfdoc_remote


def get_song_from_song_api(sheet_type, song_code, token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    #print("Getting song")
    r = requests.get(app.config['CHURCH_SONGS_URL'] + '/churchsongs/song/sheet/'+ sheet_type + '/' + song_code, headers=headers)
    #print(r.content)
    return r


def authorize_and_get_token():
#    global token_cache
#    print(token_cache)
#    if 'token' in token_cache:
#        print('used cached token')
#        ts = token_cache['timestamp']
#        print("Time Diff")
#        print(time.time() - ts)
#        if (time.time() - ts) < 900:
#            return token_cache['token']

    auth_payload = {'username': app.config['CHURCH_API_USERNAME'], 'password': app.config['CHURCH_API_PASSWORD']}
    headers = {
        'Content-Type': 'application/json'
    }
    #print("Authenticating")
    auth_response = requests.post(app.config['CHURCH_AUTH_URL'] + '/churchauth/authenticate', headers=headers,
                                 data=json.dumps(auth_payload))
    if auth_response.status_code is 200:
        auth_json = auth_response.json()
        print(auth_json)
        token = auth_json['token']
        ts = time.time()
#        token_cache = {'timestamp': ts, 'token': token}
        return token
    else:
        print('Auth Failed')
        return "ERROR"

