#!/usr/bin/env python
# File: build.py
# Description: Compile templates into a single templates.js file.


import os
import sys


def compile_templates(from_dir):
    templates_file = open(from_dir + '/js/app/templates/templates.js', 'w')
    templates_file.write("var templates = {};\n")
    os.path.walk(from_dir + '/js/app/templates', compile_templates_in_dir, templates_file)
    templates_file.close()


def compile_templates_in_dir(templates_file, directory, templates):
    template_dir_template = "templates.%(dir_name)s = {};\n"
    template_file_template = "templates.%(name)s = '%(template)s';\n"

    for template in templates:
        path = os.path.join(directory, template)
        if os.path.isfile(path) and not template.startswith('templates'):
            name = os.path.splitext(template)[0]
            print "compiling file %s" % name

            f = open(os.path.join(directory, template))
            template = f.read()
            f.close()

            template = template.replace('\n', r'\n')
            template = template.replace('\'', r'\'')

            fully_qualified_name = get_qualified_path(os.path.join(directory, name))

            templates_file.write(template_file_template %
                                 {"name": fully_qualified_name, "template": template})
        elif os.path.isdir(path):
            templates_file.write(template_dir_template %
                                 {"dir_name": get_qualified_path(path)})


def get_qualified_path(path):
    parent_dir, base_name = os.path.split(path)
    paths = [base_name]

    if base_name != 'templates':
        while not parent_dir.endswith('js/app/templates'):
            parent_dir, base_name = os.path.split(parent_dir)
            paths.append(base_name)

    paths.reverse()
    return '.'.join(paths)

if __name__ == '__main__':
    compile_templates(sys.argv[1])
