import os, sys, getopt, subprocess
USAGE = '' \
        'Usage:\n' \
        'create_project.py -r <your_project_root_dir> -n <your_project_name>\n' \
        'create_project.py --project_root=<your_project_root_dir> --project_name=<your_project_name>'

def main(argv):
    root_dir = None
    prj_nm = None
    api_url = "http://localhost:8090"
    try:
        opts, args = getopt.getopt(argv, "hr:n:a:", ["project_root=", "project_name=", "api_url="])
    except getopt.GetoptError as e:
        print(USAGE)
        print('create_project error: {}'.format(e))
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(USAGE)
            sys.exit()
        elif opt in ("-r", "--project_root"):
            root_dir = arg.strip().rstrip("\\")
        elif opt in ("-n", "--project_name"):
            prj_nm = arg
        elif opt in ("-a", "--api_url"):
            api_url = arg

    prj_dir = root_dir + '/' + prj_nm
    if os.path.exists(root_dir):
        raise RuntimeError('Project root directory {} exists!'.format(prj_dir))
        sys.exit()

    pages_dir = prj_dir + '/pages'
    static_dir = prj_dir + '/static'

    os.makedirs(prj_dir)
    os.makedirs(pages_dir)
    os.makedirs(static_dir)
    (status, output) = subprocess.getstatusoutput('virtualenv -p /usr/bin/python3 env')
    print(output)
    src_dir = ''
    (status, output) = subprocess.getstatusoutput('cp {}/config.py {}'.format(src_dir, prj_dir))
    print(output)
    (status, output) = subprocess.getstatusoutput('cp {}/main.py {}'.format(src_dir, prj_dir))
    print(output)
    (status, output) = subprocess.getstatusoutput('cp {}/config.py {}'.format(src_dir, prj_dir))
    print(output)
    (status, output) = subprocess.getstatusoutput('cp -rf {}/static {}'.format(src_dir, prj_dir))
    print(output)
    (status, output) = subprocess.getstatusoutput('touch {}/__init__.py'.format(pages_dir))
    print(output)

    config_file = prj_dir+'/config.py'

    with open(config_file, "r", encoding="utf-8") as f1, open("{}/tmp.bak", "w", encoding="utf-8") as f2:
        for line in f1:
            newline = line.replace("API_URL = 'http://localhost:8090'", "API_URL = '{}'".format(api_url))
            if newline == line:
                newline = line.replace("SECRET_KEY = 'security code not set'", "SECRET_KEY = '{} security code'".format(prj_nm))
            f2.write(newline)
    os.remove(config_file)
    os.rename('{}/tmp.bak'.format(prj_dir), 'config.py')
    os.remove('{}/tmp.bak'.format(prj_dir))

    main_file = '{}/main.py'.format(prj_dir)
    with open(main_file, "r", encoding="utf-8") as f1, open("{}/tmp.bak", "w", encoding="utf-8") as f2:
        for line in f1:
            newline = line.replace("Flask(__name__)", "Flask('{}')".format(prj_nm))
            f2.write(newline)
    os.remove(main_file)
    os.rename('{}/tmp.bak'.format(prj_dir), 'main.py')

if __name__ == "__main__":
    main(sys.argv[1:])
