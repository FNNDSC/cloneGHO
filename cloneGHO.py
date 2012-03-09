# query github
import urllib
# directory exists?
import os.path
# remove dir (and subdirs)
import shutil

# target organization
organization_exists = False;

while(organization_exists == False):
  print '\033[94m-Target organization-\033[00m'
  organization = raw_input( '<organization\'s name>: ' )
  # check if the organization exists
  f = urllib.urlopen('https://api.github.com/orgs/' + organization)
  answer = f.read()
  if (answer.find('Not Found') >= 0):
    print '\033[91m' + organization + ' does not exist or not available\033[00m\n'
  else:
    print '\033[92m' + organization + ' available\033[00m\n'
    organization_exists = True
    
# target directory
directory_exists = False;

while(directory_exists == False):
  print '\033[94m-Target Directory-\033[00m'
  directory = raw_input( '<full directory\'s name>: ' )
  if(os.path.exists(directory) == True):
    print '\033[92mTarget directory exists\033[00m'
    wait_dir_exists = os.path.exists(directory + os.sep + organization)

    if(wait_dir_exists  == True):
      print '\033[93m' + organization + ' directory already exists in ' + directory + '\033[00m'
      
      valid_input = False
      overwrite = 'n'
      confirmation = 'n'
      
      while(valid_input == False):
        overwrite = raw_input( '\033[91mDelete it?:\033[00m [y/n]' )
        if overwrite in ('y', 'n'): valid_input = True

      valid_input = False

      while(valid_input == False):
        confirmation = raw_input( '\033[91mAre you sure?:\033[00m [y/n]' )
        if confirmation in ('y', 'n'): valid_input = True


      if(confirmation == 'n'):
        wait_dir_exists = True
      else:
        if(overwrite == 'n'):
          wait_dir_exists = True
        else:
          print '\033[91mDeleting ' + directory + os.sep + organization + '\033[00m'
          shutil.rmtree(directory + os.sep + organization);
          wait_dir_exists = False

    print ''
      
    if(wait_dir_exists == False):
      print '\033[94m-Clone projects from ' + organization + '-\033[00m'
      print organization + ' will be created in ' + directory
      directory_exists = True
      # create dir
      os.mkdir(directory + os.sep + organization)
      # get info
      f2 = urllib.urlopen('https://api.github.com/orgs/' + organization + '/repos')
      answer2 = f2.read()
      found=answer2.find('clone_url')
      while found > -1:
        begin=answer2.find('https', found+1);
        end=answer2.find('\"', begin+1);

        address = answer2[begin:end]


        namepos = answer2.find('\"name\"', end+1)
        beginname = answer2.find('\"', namepos+7)
        endname = answer2.find('\"', beginname+1)

        name = answer2[beginname+1:endname]

        # pull
        os.system('git clone ' + address + ' ' + directory + os.sep + organization + os.sep + name)             
        found=answer2.find('clone_url', end+1)

  else:
    print '\033[93mTarget directory does not exist\033[00m\n'
