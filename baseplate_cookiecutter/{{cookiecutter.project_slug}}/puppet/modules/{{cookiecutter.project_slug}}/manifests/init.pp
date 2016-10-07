class {{ cookiecutter.project_slug }} {
  exec { 'add reddit ppa':
    command => 'add-apt-repository -y ppa:reddit/ppa',
    unless  => 'apt-cache policy | grep reddit/ppa',
    notify  => Exec['update apt cache'],
  }

  $dependencies = [
    {%- for dep in cookiecutter.dependencies.apt: %}
    '{{ dep }}',
    {%- endfor %}
  ]

  package { $dependencies:
    ensure => installed,
    before => Exec['build app'],
  }

  exec { 'build app':
    user    => $::user,
    cwd     => $::project_path,
    command => 'python setup.py build',
    before  => Exec['install app'],
  }

  exec { 'install app':
    user    => $::user,
    cwd     => $::project_path,
    command => 'python setup.py develop --user',
  }
}
