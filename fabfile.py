#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Zuza Software Foundation
# Copyright 2013 Aneesh Dogra (aneesh@activitycentral.com)

"""Fabric deployment file."""

from os.path import isfile, isdir, dirname
from os import makedirs
from os.path import exists as path_exists

from fabric.api import cd, env
from fabric.context_managers import hide, prefix, settings
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, upload_template
from fabric.operations import require, run, sudo, put, get

#
# Deployment environments
#

def production():
    """Work on the production environment"""

    try:
        from deploy.production import fabric
    except ImportError:
        print("Can't load 'production' environment; is PYTHONPATH exported?")
        exit(1)

    env.update(fabric.SETTINGS)
    env.environment = 'production'


#
# Commands
#


def _init_directories():
    """Creates initial directories"""
    if exists('%(project_path)s' % env):
        sudo('rm -rf %(project_path)s' % env)

    sudo('mkdir -p %(project_path)s' % env)
    sudo('mkdir -p %(project_path)s/logs' % env)
    sudo('chmod -R g=u '
         '%(project_path)s' % env)
    sudo('chown -R %(user)s:%(server_group)s '
         '%(project_path)s' % env)


def _init_virtualenv():
    """Creates initial virtualenv"""
    run('virtualenv -p %(python)s --no-site-packages %(env_path)s' % env)
    with prefix('source %(env_path)s/bin/activate' % env):
        run('easy_install pip')


def _clone_repo():
    """Clones the Git repository"""
    run('git clone %(project_repo)s %(project_repo_path)s' % env)


def _checkout_repo(branch="master"):
    """Updates the Git repository and checks out the specified branch"""
    with cd(env.project_repo_path):
        run('git checkout master')
        run('git pull')
        run('git checkout %s' % branch)
    run('chmod -R go=u,go-w %(project_repo_path)s' % env)


def _install_requirements():
    """Installs dependencies defined in the requirements file"""
    with prefix('source %(env_path)s/bin/activate' % env):
        run('pip install -r %(project_repo_path)s/requirements.pip' % env)
    run('chmod -R go=u,go-w %(env_path)s' % env)


def _update_requirements():
    """Updates dependencies defined in the requirements file"""
    with prefix('source %(env_path)s/bin/activate' % env):
        run('pip install -U -r %(project_repo_path)s/requirements.pip' % env)
    run('chmod -R go=u,go-w %(env_path)s' % env)


def bootstrap(branch="master"):
    """Bootstraps a Pootle deployment using the specified branch"""
    require('environment', provided_by=production)

    if (not exists('%(project_path)s' % env) or
        confirm('\n%(project_path)s already exists. Do you want to continue?'
                % env, default=False)):

            print('Bootstrapping initial directories...')

            with settings(hide('stdout', 'stderr')):
                _init_directories()
                _init_virtualenv()
                _clone_repo()
                run("touch %(project_repo_path)s/../__init__.py" % env)
                _checkout_repo(branch=branch)
                _install_requirements()
    else:
        print('Aborting.')


def _create_db_mysql():
    require('environment', provided_by=production)

    create_db_cmd = ("CREATE DATABASE `%(db_name)s` "
                     "DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
                     % env)
    grant_db_cmd = ("GRANT ALL PRIVILEGES ON `%(db_name)s`.* TO `%(db_user)s`"
                    "@localhost IDENTIFIED BY \"%(db_password)s\"; "
                    "FLUSH PRIVILEGES;"
                    % env)

    with settings(hide('stderr')):
        run(("mysql -u %(db_user)s %(db_password_opt)s -e '" % env) +
            create_db_cmd +
            ("' || { test root = '%(db_user)s' && exit $?; }" % env))

def _create_db_sqlite3():
    db_path = env.db_name
    db_dir  = dirname(db_path)
    try:
        makedirs(db_dir)
    except OSError:
        pass
    run("touch %s" % db_path)
    sudo("chown -R %s:%s %s" % (env.user, env.server_group, db_dir))
    sudo("chmod -R g+w %s" % (db_dir)) # mark the db writable

def _get_database_type(database):
    if env.db_engine == "django.db.backends.sqlite3":
        return "sqlite3"
    elif env.db_engine == "django.db.backends.mysql":
        return "mysql"

def create_db():
    """Creates a new DB"""
    require('environment', provided_by=production)

    db_type = _get_database_type()
    if db_type == 'mysql':
        _create_db_mysql()
    elif db_type == 'sqlite3':
        _create_db_sqlite3(database)
    else:
        print("The database type is not currently supported by our fabfile. You'll have to create it manually.")

def drop_db():
    """Drops the current DB - losing all data!"""
    require('environment', provided_by=production)
    db_type = _get_database_type()

    if confirm('\nDropping the %s DB loses ALL its data! Are you sure?'
               % (env['db_name']), default=False):
        if db_type == 'mysql':
            _drop_db_mysql()
        elif db_type == 'sqlite3':
            _drop_db_sqlite3(database)
    else:
        print('Aborting.')


def _drop_db_mysql():
    run("echo 'DROP DATABASE `%s`' | mysql -u %s %s" %
            (env['db_name'], env['db_user'], env['db_password_opt']))

def _drop_db_sqlite3(database):
    run("rm %s" % database['NAME'])

def setup_db():
    """Runs all the necessary steps to create the DB schema from scratch"""
    require('environment', provided_by=production)
    syncdb()


def syncdb():
    """Runs `syncdb` to create the DB schema"""
    require('environment', provided_by=production)
    with cd('%(project_repo_path)s' % env):
        with prefix('source %(env_path)s/bin/activate' % env):
            run('python manage.py syncdb')

def load_db(dumpfile=None):
    """Loads data from a SQL script to Pootle DB"""
    require('environment', provided_by=[production, staging])

    if dumpfile is not None:
        if isfile(dumpfile):
            remote_filename = '%(project_path)s/DB_backup_to_load.sql' % env

            if (not exists(remote_filename) or
                confirm('\n%s already exists. Do you want to overwrite it?'
                        % remote_filename, default=False)):

                    print('\nLoading data into the DB...')

                    with settings(hide('stderr')):
                        put(dumpfile, remote_filename)
                        run('mysql -u %s %s %s < %s' %
                            (env['db_user'], env['db_password_opt'],
                             env['db_name'], remote_filename))
                        run('rm %s' % (remote_filename))
            else:
                print('\nAborting.')
        else:
            print('\nERROR: The file "%s" does not exist. Aborting.' % dumpfile)
    else:
        print('\nERROR: A (local) dumpfile must be provided. Aborting.')


def dump_db(dumpfile="pathagarh_DB_backup.sql"):
    """Dumps the DB as a SQL script and downloads it"""
    require('environment', provided_by=[production, staging])

    if isdir(dumpfile):
        print("dumpfile '%s' is a directory! Aborting." % dumpfile)

    elif (not isfile(dumpfile) or
          confirm('\n%s already exists locally. Do you want to overwrite it?'
                  % dumpfile, default=False)):

              remote_filename = '%s/%s' % (env['project_path'], dumpfile)

              if (not exists(remote_filename) or
                  confirm('\n%s already exists. Do you want to overwrite it?'
                          % remote_filename, default=False)):

                      print('\nDumping DB...')

                      with settings(hide('stderr')):
                          run('mysqldump -u %s %s %s > %s' %
                              (env['db_user'], env['db_password_opt'],
                               env['db_name'], remote_filename))
                          get(remote_filename, '.')
                          run('rm %s' % (remote_filename))
              else:
                  print('\nAborting.')
    else:
        print('\nAborting.')


def update_code(branch="master"):
    """Updates the source code and its requirements"""
    require('environment', provided_by=production)

    print('Getting the latest code and dependencies...')

    with settings(hide('stdout', 'stderr')):
        _checkout_repo(branch=branch)
        _update_requirements()

def deploy(branch="master"):
    """Updates the code and installs the production site"""
    require('environment', provided_by=production)

    print('Deploying the site...')

    with settings(hide('stdout', 'stderr')):
        update_code(branch=branch)
        install_site()


def install_site():
    """Configures the server and enables the site"""
    require('environment', provided_by=production)

    print('Configuring and installing site...')

    with settings(hide('stdout', 'stderr')):
        update_config()
        enable_site()


def update_config():
    """Updates server configuration files"""
    require('environment', provided_by=production)

    with settings(hide('stdout', 'stderr')):

        # Configure VirtualHost
        upload_template('deploy/%(environment)s/virtualhost.conf' % env,
                        env.vhost_file, context=env, use_sudo=True)

        # Configure and install settings
        upload_template('deploy/%(environment)s/settings.conf' % env,
                        '%(project_settings_path)s'
                        % env, context=env)


def enable_site():
    """Enables the site"""
    require('environment', provided_by=production)

    with settings(hide('stdout', 'stderr')):
        _switch_site(True)


def disable_site():
    """Disables the site"""
    require('environment', provided_by=production)

    with settings(hide('stdout', 'stderr')):
        _switch_site(False)


def _switch_site(enable):
    """Switches site's status to enabled or disabled"""

    action = "Enabling" if enable else "Disabling"
    print('%s site...' % action)

    env.apache_command = 'a2ensite' if enable else 'a2dissite'
    sudo('%(apache_command)s %(project_name)s' % env)
    sudo('service apache2 reload')


def touch():
    """Reloads daemon processes by touching the WSGI file"""
    require('environment', provided_by=[production, staging])

    print('Running touch...')

    with settings(hide('stdout', 'stderr')):
        run('touch %(wsgi_file)s' % env)
