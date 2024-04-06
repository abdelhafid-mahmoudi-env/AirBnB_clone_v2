# Puppet manifest to setup web servers for deployment of web_static

file { '/etc/nginx/sites-available/default':
    ensure => file,
    content => template('nginx-default.erb'),
    require => Package['nginx'],
    notify  => Service['nginx'],
}

file { '/data/web_static/releases/test/index.html':
    ensure  => file,
    content => "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>",
    require => File['/data/web_static/releases/test'],
    notify  => Service['nginx'],
}

file { '/data/web_static/current':
    ensure => link,
    target => '/data/web_static/releases/test',
    require => File['/data/web_static/releases/test/index.html'],
    notify  => Service['nginx'],
}

exec { 'chown-data':
    command => 'chown -R ubuntu:ubuntu /data/',
    path    => ['/bin', '/usr/bin/'],
}
