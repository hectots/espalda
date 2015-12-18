#!/usr/bin/env python
# File: build.py
# Description: Compile templates into a single templates.js file.


import os
import sys


def compile_templates(from_dir, to_dir):
    template_file_template = "templates.%(dir_name)s.%(name)s = '%(template)s';\n"

    templates_file = open(to_dir + '/js/app/templates/templates.js', 'w')

    templates_file.write("var templates = {};\n")

    for directory in os.listdir(from_dir + '/js/app/templates'):
        if directory != "templates.js":

            templates_file.write("\ntemplates.%(directory)s = {};\n \n" % {"directory": directory})

            for template in os.listdir(from_dir + '/js/app/templates/' + directory):
                name = os.path.splitext(template)[0]
                print "compiling file %s" % name

                f = open(from_dir + '/js/app/templates/' + directory + "/" + template)
                template = f.read()
                f.close()

                template = template.replace('\n', r'\n')
                template = template.replace('\'', r'\'')

                templates_file.write(template_file_template %
                                     {"name": name, "template": template, "dir_name": directory})
    templates_file.close()


if __name__ == '__main__':
    compile_templates(sys.argv[1], sys.argv[1])
