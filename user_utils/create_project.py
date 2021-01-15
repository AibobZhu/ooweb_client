import os, sys, getopt, subprocess

USAGE = '''
Usage:
    create_project.py [-r|--project_root] <your_project_root_dir> [-n|project_name] <your_project_name> [-u|--api_url] <api_url in http://xxxx:xxxx format>
'''


def main(argv):
    root_dir = None
    prj_nm = None
    api_url = "http://localhost:8090"

    try:
        opts, args = getopt.getopt(argv, "hr:n:u:", ["project_root=", "project_name=", "api_url="])
    except getopt.GetoptError as e:
        print(USAGE)
        print('create_project error: {}'.format(e))
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(USAGE)
            sys.exit()
        elif opt in ("-r", "--project_root"):
            root_dir = os.path.realpath(arg.strip().rstrip("/"))
        elif opt in ("-n", "--project_name"):
            prj_nm = arg
        elif opt in ("-u", "--api_url"):
            api_url = arg
    if not root_dir:
        print('create_project error: project_root is NOT valid!')
        print(USAGE)
        sys.exit(3)
    if not prj_nm:
        print('Error: project_name is NOT valid')
        print(USAGE)
        sys.exit(4)

    prj_dir = root_dir + '/' + prj_nm
    if os.path.exists(prj_dir):
        raise RuntimeError('Project directory {} exists!'.format(prj_dir))
        sys.exit()

    pages_dir = prj_dir + '/pages'
    static_dir = prj_dir + '/static'
    config_file = prj_dir+'/config.py'
    src_dir = '/'.join(os.path.realpath(__file__).split('/')[0:-1]) + '/new_project'

    print('Make director: {}'.format(prj_dir))
    os.makedirs(prj_dir)
    os.makedirs(pages_dir)
    os.makedirs(static_dir)
    print('Enter director:{}'.format(prj_dir))
    os.chdir(prj_dir)
    (status, output) = subprocess.getstatusoutput('virtualenv -p /usr/bin/python3 venv')
    print(output)
    print('Copy project templates')
    (status, output) = subprocess.getstatusoutput('cp -rf {}/* .'.format(src_dir))
    print(output)
    print('Active virtualenv')
    (status, output) = subprocess.getstatusoutput('. venv/bin/activate;pip install -r requirements.txt')
    print(output)

    with open(config_file, "r", encoding="utf-8") as f1, open("{}/tmp.bak".format(prj_dir), "w", encoding="utf-8") as f2:
        for line in f1:
            newline = line.replace("API_URL = 'http://localhost:8090'", "API_URL = '{}'".format(api_url))
            if newline == line:
                newline = line.replace("SECRET_KEY = 'security code not set'", "SECRET_KEY = '{} security code'".format(prj_nm))
            f2.write(newline)
    os.remove(config_file)
    os.rename('{}/tmp.bak'.format(prj_dir), 'config.py')
    #os.remove('{}/tmp.bak'.format(prj_dir))

    main_file = '{}/main.py'.format(prj_dir)
    with open(main_file, "r", encoding="utf-8") as f1, open("{}/tmp.bak".format(prj_dir), "w", encoding="utf-8") as f2:
        for line in f1:
            #newline = line.replace("Flask(__name__)", "Flask('{}')".format(prj_nm))
            newline = line.replace("project_name = 'not set yet'", "project_name = '{}'".format(prj_nm))
            f2.write(newline)
    os.remove(main_file)
    os.rename('{}/tmp.bak'.format(prj_dir), 'main.py')


if __name__ == "__main__":
    main(sys.argv[1:])
