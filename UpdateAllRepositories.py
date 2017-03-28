import os
import subprocess
import time
import logging
from re import sub


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='SVNUpdate.log',
                    filemode='a')

startupinfo = None

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW


def main():
    if is_svn_installed():
        update_all_repo()
    else:
        print('Please install SVN command line tools to use this application')


def is_svn_installed():
    cmd = 'svn --version'
    try:
        subprocess.Popen(cmd, startupinfo=startupinfo)
        return True
    except Exception as e:
        return False

        
def update_all_repo():
    logging.info('Update started @ : {}'.format(time.asctime(time.localtime(time.time()))))
    
    count = 0

    print('Collecting SVN repositories')
    
    for root, dirs, files in os.walk(".", topdown=False):
        for name in dirs:
            if name == '.svn':
                count += 1
                svnDir = os.path.join(root, name)[2:-5]
                print('Updating ' + svnDir)
                cmd = 'svn up "' + svnDir + '"'
                try:
                    p = subprocess.Popen(cmd, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    pout, _ =  p.communicate()
                    pout = sub('[\n\r]', '', pout.decode('utf-8'))
                    pout = sub('[:]', ' is ', pout)
                    logging.info('{}'.format(pout))
                    p.wait()
                except Exception as e:
                    print('Whoops !! Something went wrong, check log for more info')
                    logging.error('{}'.format(e))
                
    print('Total svn repositories updated : {}'.format(str(count)))
    logging.info('Total svn repositories updated : {}'.format(str(count)))
    logging.info('Update done @ : {}'.format(time.asctime(time.localtime(time.time()))))
    logging.shutdown()

if __name__ == '__main__':
    main()
