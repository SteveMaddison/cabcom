# === Class cabcom
#
# Module to set up Cabcom development environment.
#
# === Authors
#
# Steve Maddison <steve@cosam.org>
#
# === Copyright
#
# Copyright 2014 Steve Maddison
#
class cabcom (
) {
  case $::operatingsystem {
    /^(Debian|Ubuntu)$/: {
      $packages = [
        'git',
        'python',
        'python-pip',
        'python-yaml',
	'rabbitmq-server',
        'sqlite3',
        'vim',
      ]
    }
    default: {
      warning("Operating system '$::operatingsystem' not supported.")
    }
  }

  package { $packages: }

  package { ['django','celery','django-celery']:
    provider => 'pip',
    require  => Package['python-pip'],
  }

  if $vagrant {
    # Link to the sources.
    file { '/home/vagrant/cabcom':
      ensure => link,
      target => '/vagrant',
    }
  }
}

