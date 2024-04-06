exec {'nginx installation':
  provider => shell,
  command  => 'sudo apt-get -y install nginx',
}

exec {'update packages':
  provider => shell,
  command  => 'sudo apt-get -y update',
  before   => Exec['start Nginx'],
}

exec {'start Nginx':
  provider => shell,
  command  => 'sudo service nginx start',
  require  => Exec['nginx installation'],
}

exec {'create first directory':
  provider => shell,
  command  => 'sudo mkdir -p /data/web_static/releases/test/',
}

exec {'create second directory':
  provider => shell,
  command  => 'sudo mkdir -p /data/web_static/shared/',
}

exec {'content into html':
  provider => shell,
  command  => 'echo "Test" | sudo tee /data/web_static/releases/test/index.html',
}

exec {'symbolic link':
  provider => shell,
  command  => 'sudo ln -sf /data/web_static/releases/test/ /data/web_static/current',
  require  => Exec['content into html'],
}

exec {'put location':
  provider => shell,
  command  => 'sudo sed -i \'38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n\' /etc/nginx/sites-available/default',
  require  => Exec['symbolic link'],
}

exec {'restart Nginx':
  provider => shell,
  command  => 'sudo service nginx restart',
  require  => Exec['put location'],
}

exec {'create index.html':
  provider => shell,
  command  => 'echo "Hello, World!" | sudo tee /data/web_static/current/index.html',
  require  => Exec['symbolic link'],
}

file {'/data/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}
