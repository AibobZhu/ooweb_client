import os, sys, getopt, subprocess

USAGE = 'Usage:' \
        'under your project root directory, execute:' \
        '"create_page.py -n <new page name> -u <new page rule url> [-p <your project root directory>]"' \
        'Note:' \
        '    page naming should follow the naming rule of class in Python.'


def main(argv):

    prj_root_dir = os.getenv('OWWWO_ROOT')
    prj_pages_dir = '{}/pages'.format(prj_root_dir)
    pages_init_file = '{}/__init__.py'.format(prj_pages_dir)
    page_name = None
    page_rule = None
    src_dir = '/home/ubuntu/PycharmProjects/ooweb_client/user_utils/new_project/pages/'

    try:
        opts, args = getopt.getopt(argv,"hn:r:u:",["page_name=", "project_root=", "page_rule="])
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
        elif opt in ("-u", "--page_url"):
            page_rule = arg
            if not arg:
                print('Error: please input valid value of -u or --page_url')
                print(USAGE)
                sys.exit()

    pwd = os.getcwd()
    if pwd != prj_root_dir and pwd != prj_pages_dir:
        print('Error: current directory:"{}" is not your project root directory or "pages" subdirectory.'\
            'Your project root directory is: "{}"'.format(pwd, prj_root_dir))
        print(USAGE)
        sys.exit()

    (status, output) = subprocess.getstatusoutput('cp {}/new_page.py {}/pages/'.format(src_dir, prj_root_dir))
    print(status)
    if status != 0:
        print('Error: copy file template from:"{}" to :"{}/pages/{}.py" failed'.format(src_dir+'/new_page.py', prj_root_dir, page_name))
        sys.exit()
    print(output)

    new_page_file = '{}/pages/new_page.py'.format(prj_root_dir)
    with open(new_page_file, "r", encoding="utf-8") as f1, open("{}/tmp.bak".format(prj_root_dir), "w", encoding="utf-8") as f2:
        for line in f1:
            newline = line.replace("OONewPage", "{}".format(page_name)).replace("/oonewpage_rule_not_set", page_rule)
            f2.write(newline)
    os.remove(new_page_file)
    os.rename('{}/tmp.bak'.format(prj_root_dir), '{}/pages/{}.py'.format(prj_root_dir, page_name))

    if not os.path.exists(pages_init_file):
        (status, output) = subprocess.getstatusoutput('cp {}/__init__.py {}/pages/'.format(src_dir, prj_root_dir))
        if status != 0:
            print('Error: copy file template from:"{}" to :"{}/pages/" failed'.format(
                src_dir+'/__init__.py', prj_root_dir
            ))
            sys.exit()
        print(output)
    with open(pages_init_file, "r", encoding="utf-8") as f1, open("{}/tmp.bak".format(prj_root_dir), "w", encoding="utf-8") as f2:
        newline = "import pages.{}\n".format(page_name)
        for line in f1:
           f2.write(line)
           if line.find('#import all pages') >= 0:
               f2.write(newline)
    os.remove(pages_init_file)
    os.rename('{}/tmp.bak'.format(prj_root_dir), '{}/pages/__init__.py'.format(prj_root_dir))

if __name__ == "__main__":
    main(sys.argv[1:])
