exec { 'apt_update':
  command     => '/usr/bin/env apt-get -y update',
}

exec { 'install_nginx':
  command     => '/usr/bin/env apt-get -y install nginx',
  require     => Exec['apt_update'],
}

exec { 'configure_nginx':
  command     => '/usr/bin/env sed -i "/listen \[::\]:80 default_server/ a\\\trewrite ^/redirect_me https://www.youtube.com/watch?v=QH2-TGUlwu4 permanent;" /etc/nginx/sites-available/default',
  notify      => Exec['start_nginx'],
}

exec { 'add_header_to_nginx':
  command     => '/usr/bin/env sed -i "/listen \[::\]:80 default_server/ a\\\tadd_header X-Served-By \"\$HOSTNAME\";" /etc/nginx/sites-available/default',
  notify      => Exec['start_nginx'],
}

exec { 'configure_error_page':
  command     => '/usr/bin/env sed -i "/redirect_me/ a\\\terror_page 404 /custom_404.html;" /etc/nginx/sites-available/default',
  notify      => Exec['start_nginx'],
}

exec { 'create_custom_404_page':
  command     => '/usr/bin/env echo "Ceci n\'est pas une page" > /var/www/html/custom_404.html',
}

exec { 'start_nginx':
  command     => '/usr/bin/env service nginx start',
  require     => Exec['configure_nginx', 'add_header_to_nginx', 'configure_error_page'],
}

exec { 'create_web_static_directories':
  command     => '/usr/bin/env mkdir -p /data/web_static/releases/test/ && /usr/bin/env mkdir -p /data/web_static/shared/',
}

exec { 'create_test_index_html':
  command     => '/usr/bin/env echo "simple content, to test your Nginx configuration" > /data/web_static/releases/test/index.html',
}

exec { 'link_current_to_test':
  command     => '/usr/bin/env ln -sf /data/web_static/releases/test/ /data/web_static/current',
}

exec { 'configure_nginx_static_location':
  command     => '/usr/bin/env sed -i "/^\tlocation \/ {$/ i\\\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n}" /etc/nginx/sites-available/default',
  notify      => Exec['restart_nginx'],
}

exec { 'restart_nginx':
  command     => '/usr/bin/env service nginx restart',
}

exec { 'set_permissions':
  command     => '/usr/bin/env chown -R ubuntu:ubuntu /data/',
}
