#!/usr/bin/env python
import os
import sys
import urllib2
from zipfile import ZipFile


def execute_command(command, params):
    if command == 'create':
        if params is not None and len(params) >= 1:
            create_project(' '.join(params))


def create_project(project_name):
    copy_h5bp_to_project(project_name)
    create_js_directory_structure(project_name)
    create_app(project_name)
    update_main(project_name)


def copy_h5bp_to_project(project_name):
    response = urllib2.urlopen('http://www.initializr.com/builder?boot-hero&jquerymin&h5bp-iecond&h5bp-chromeframe&h5bp-analytics&h5bp-favicon&h5bp-appletouchicons&modernizrrespond&izr-emptyscript&boot-css&boot-scripts')
    h5bp = response.read()
    h5bp_zip = open('h5bp.zip', 'w')
    h5bp_zip.write(h5bp)
    h5bp_zip.close()
    h5bp_zip_file = ZipFile('h5bp.zip', 'r')
    h5bp_zip_file.extractall()
    os.rename('initializr', to_lower_case(project_name))
    os.remove('h5bp.zip')


def create_js_directory_structure(project_name):
    project_name = to_lower_case(project_name)
    os.makedirs(project_name + '/js/app/collections')
    os.makedirs(project_name + '/js/app/controllers')
    os.makedirs(project_name + '/js/app/models')
    os.makedirs(project_name + '/js/app/routers')
    os.makedirs(project_name + '/js/app/templates')
    os.makedirs(project_name + '/js/app/views')


def create_app(project_name):
    app_js_template = """var %(project_name)s = {
    Models: {},
    Collections: {},
    Views: {},
    Routers: {},
    Controllers: {},

    init: function () {
        'use strict';

        Backbone.history.start();
    }
};"""

    app_js_contents = app_js_template % {'project_name': to_camel_case(project_name)}
    app_js = open(to_lower_case(project_name) + '/js/app/app.js', 'w')
    app_js.write(app_js_contents)
    app_js.close()


def update_main(project_name):
    main_js_template = """$(document).ready(function () {
    'use strict';
    %(project_name)s.init();
});"""

    main_js_contents = main_js_template % {'project_name': to_camel_case(project_name)}
    main_js = open(to_lower_case(project_name) + '/js/main.js', 'w')
    main_js.write(main_js_contents)
    main_js.close()


def to_lower_case(s):
    return ''.join([word.lower() for word in s.split(' ')])


def to_camel_case(s):
    return ''.join([word.title() for word in s.split(' ')])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1]
        params = sys.argv[2:] if len(sys.argv[1:]) > 1 else None
        execute_command(command, params)
