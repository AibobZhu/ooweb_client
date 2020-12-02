import os, sys, getopt, subprocess

prj_root_dir = os.getenv('OWWWO_ROOT')
prj_pages_dir = '{}/pages'.format(prj_root_dir)
pages_init_file = '{}/__init__.py'.format(prj_pages_dir)
page_name = None
page_rule = None

USAGE = 'Usage:' \
        'under your project root directory, execute:' \
        '"create_page.py -n <new page name> -u <new page rule url> [-p <your project root directory>]"' \
        'Note:' \
        '    page naming should follow the naming rule of class in Python.'


def main(argv):

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
        elif opt in ("-r", "--project_root"):
            prj_root_dir = arg
        elif opt in ("-u", "--page_url"):
            page_rule = arg

    pwd = os.path.dirname(__file__)
    if pwd != prj_root_dir or pwd != prj_pages_dir:
        print('Error: current directory:"{}" is not your project root directory or "pages" subdirectory.'\
            'Your project root directory is: "{}"'.format(prj_root_dir))
        print(USAGE)
        sys.exit()

    src_dir = ''
    (status, output) = subprocess.getstatusoutput('cp {}/pages/new_page.py {}/pages/{}.py'.format(src_dir, prj_root_dir, page_name))
    print(output)
    new_page_file = '{}/pages/{}.py'.format(prj_root_dir, page_name)
    with open(new_page_file, "r", encoding="utf-8") as f1, open("{}/tmp.bak".format(prj_root_dir), "w", encoding="utf-8") as f2:
        for line in f1:
            newline = line.replace("OONewPage", "{}".format(page_name))
            if newline == line:
               newline = line.replace("/oonewpage_rule_not_set", page_rule)
            f2.write(newline)
    os.remove(new_page_file)
    os.rename('{}/tmp.bak'.format(prj_root_dir), '{}.py'.format(page_name))
    os.remove('{}/tmp.bak'.format(prj_root_dir))

if __name__ == "__main__":
    main(sys.argv[1:])
