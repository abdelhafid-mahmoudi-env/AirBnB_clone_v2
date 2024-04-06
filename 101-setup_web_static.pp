# Puppet manifest to set up web servers for deployment of web_static

# Define parameters
$nginx_config_file = '/etc/nginx/sites-available/default'
$web_static_dir = '/data/web_static'
$release_dir = "${web_static_dir}/releases/test"
$index_file_path = "${release_dir}/index.html"
$nginx_service = 'nginx'
$nginx_package = 'nginx'
$web_owner = 'ubuntu'
$web_group = 'ubuntu'

# Install Nginx package
package { $nginx_package:
    ensure => installed,
}

# Ensure Nginx configuration file is present and correctly configured
file { $nginx_config_file:
    ensure => file,
    content => template('nginx-default.erb'),
    require => Package[$nginx_package],
    notify  => Service[$nginx_service],
}

# Create the directory structure for web_static
file { [$web_static_dir, $release_dir]:
    ensure => directory,
    owner  => $web_owner,
    group  => $web_group,
}

# Create index.html file for the test deployment
file { $index_file_path:
    ensure  => file,
    content => "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>",
    owner   => $web_owner,
    group   => $web_group,
    require => File[$release_dir],
    notify  => Service[$nginx_service],
}

# Create a symbolic link to the current deployment
file { "${web_static_dir}/current":
    ensure => link,
    target => $release_dir,
    require => File[$index_file_path],
    notify  => Service[$nginx_service],
}

# Change ownership of the /data directory recursively to the ubuntu user
exec { 'chown-web':
    command => "chown -R ${web_owner}:${web_group} ${web_static_dir}",
    onlyif  => "test ! -w ${web_static_dir}",
}
