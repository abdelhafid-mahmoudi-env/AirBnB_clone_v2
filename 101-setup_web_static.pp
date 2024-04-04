# 101-setup_web_static.pp

# Define class for setting up web_static
class web_static_setup {

  # Ensure the required directories are created
  file { '/data':
    ensure => 'directory',
  }

  file { '/data/web_static':
    ensure => 'directory',
  }

  file { '/data/web_static/releases':
    ensure => 'directory',
  }

  file { '/data/web_static/shared':
    ensure => 'directory',
  }

  # Create a symbolic link for 'current'
  file { '/data/web_static/current':
    ensure  => 'link',
    target  => '/data/web_static/releases/test',
    require => File['/data/web_static'],
  }

  # Create index.html
  file { '/data/web_static/releases/test/index.html':
    ensure  => 'file',
    content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
    require => File['/data/web_static/releases/test'],
  }
}

# Apply the class
include web_static_setup
