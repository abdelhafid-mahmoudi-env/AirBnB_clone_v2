# 101-setup_web_static.pp

# Ensure Nginx package is installed
package { 'nginx':
  ensure => installed,
}

# Define directories
file { '/data':
  ensure => directory,
}

file { '/data/web_static':
  ensure => directory,
  owner  => 'root',
  group  => 'root',
}

file { '/data/web_static/releases':
  ensure => directory,
  owner  => 'root',
  group  => 'root',
}

file { '/data/web_static/shared':
  ensure => directory,
  owner  => 'root',
  group  => 'root',
}

file { '/data/web_static/releases/test':
  ensure => directory,
  owner  => 'root',
  group  => 'root',
}

# Create a fake HTML file for testing
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '<html><head></head><body>Holberton School</body></html>',
  owner   => 'root',
  group   => 'root',
}

# Create a symbolic link
file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test',
  owner   => 'root',
  group   => 'root',
}

# Restart Nginx service
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/data/web_static/current'],
}
