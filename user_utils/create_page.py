import os, sys, getopt, subprocess

USAGE = '''
Usage:
    create_page.py [-n|--page_name] <new page name> [-u|--page_urls] <new page rule urls like 'rule1,rule2,...'> [-r|--project_root] <your project root directory>
    Note: page naming should follow the naming rule of class in Python.
'''


def main(argv):

    prj_root_dir = os.getenv('OWWWO_ROOT')
    prj_pages_dir = '{}/pages'.format(prj_root_dir)
    pages_init_file = '{}/__init__.py'.format(prj_pages_dir)
    page_name = None
    page_rules = None
    src_dir = '/'.join(os.path.realpath(__file__).split('/')[0:-1])

    try:
        opts, args = getopt.getopt(argv,"hn:r:u:",["page_name=", "project_root=", "page_urls="])
    except getopt.GetoptError as e:
        print(e)
        print(USAGE)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(USAGE)
            sys.exit()
        elif opt in ("-n", "--page_name"):
            page_name = arg
            if not arg:
                print('Error: please input valid value of -n or --page_name')
                print(USAGE)
                sys.exit()
        elif opt in ("-r", "--project_root"):
            prj_root_dir = os.path.abspath(arg)
            if not arg:
                print('Error: please input valid value of -r or --project_root')
                print(USAGE)
                sys.exit()
            prj_pages_dir = '{}/pages'.format(prj_root_dir)
            pages_init_file = '{}/__init__.py'.format(prj_pages_dir)
        elif opt in ("-u", "--page_urls"):
            rules = arg.split(',')
            page_rules = ','.join(rules)
            if not arg:
                print('Error: please input valid value of -u or --page_urls')
                print(USAGE)
                sys.exit()

    '''
    pwd = os.getcwd()
    if pwd != prj_root_dir and pwd != prj_pages_dir:
        print('Error: current directory:"{}" is not your project root directory or "pages" subdirectory.'\
            'Your project root directory is: "{}"'.format(pwd, prj_root_dir))
        print(USAGE)
        sys.exit()
    '''
    if not prj_root_dir:
        print('Error: project_root is not valid!')
        print(USAGE)
        sys.exit(2)
    if not page_rules:
        print('Error: page_rules is not valid!')
        print(USAGE)
        sys.exit(3)
    if not page_name:
        print('Error: page_name is not valid!')
        print(USAGE)
        sys.exit(4)

    page_file = prj_pages_dir+'/'+page_name+'.py'
    if not os.path.exists(page_file):
        (status, output) = subprocess.getstatusoutput('cp {}/new_page.py {}'.format(src_dir, prj_pages_dir))
        print(status)
        if status != 0:
            print('Error: copy file template from:"{}" to :"{}/{}.py" failed'.
                  format(src_dir+'/new_page.py', prj_pages_dir, page_name))
            sys.exit()
        print(output)

        new_page_file = '{}/new_page.py'.format(prj_pages_dir)
        with open(new_page_file, "r", encoding="utf-8") as f1, open("{}/tmp.bak".format(prj_root_dir), "w", encoding="utf-8") as f2:
            for line in f1:
                newline = line.replace("OONewPage", "{}".format(page_name))
                f2.write(newline)
        os.remove(new_page_file)
        os.rename('{}/tmp.bak'.format(prj_root_dir), '{}/{}.py'.format(prj_pages_dir, page_name))
    else:
        return

    if not os.path.exists(pages_init_file):
        (status, output) = subprocess.getstatusoutput('cp {}/new_project/pages/__init__.py {}/'.
                                                      format(src_dir, prj_pages_dir))
        if status != 0:
            print('Error: copy file template from:"{}/new_project/pages/__init__.py" to :"{}" failed'.format(
                src_dir, prj_pages_dir
            ))
            sys.exit()
        print(output)

    with open(pages_init_file, "r", encoding="utf-8") as f1, open("{}/tmp.bak".format(prj_root_dir), "w", encoding="utf-8") as f2:
        newline1 = "from pages.{} import {}\n".format(page_name, page_name)
        newline1_wrote = False
        newline2 = "    {}.register(app=app, rules=[{}], name='{}', top_menu=BasePage.top_menu)\n".format(
            page_name, page_rules,page_name)
        newline2_wrote = False
        for line in f1:
           f2.write(line)
           if line.find('#import all pages') >= 0 and not newline1_wrote:
               f2.write(newline1)
               newline1_wrote = True
           if line.find('def register(app):') >= 0 and not newline2_wrote:
               f2.write(newline2)
               newline2_wrote = True

    os.remove(pages_init_file)
    os.rename('{}/tmp.bak'.format(prj_root_dir), '{}/__init__.py'.format(prj_pages_dir))

if __name__ == "__main__":
    main(sys.argv[1:])
