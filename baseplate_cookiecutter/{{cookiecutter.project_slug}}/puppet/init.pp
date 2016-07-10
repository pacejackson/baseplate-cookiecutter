Exec { path => [ '/usr/bin', '/usr/sbin', '/bin', '/usr/local/bin' ] }

exec { 'update apt cache':
  command     => 'apt-get update',
  refreshonly => true,
}

# make updating the apt cache an implicit requirement for all packages
Exec['update apt cache'] -> Package<| |>

include {{ cookiecutter.project_slug }}

{%- for puppet_module in cookiecutter.puppet_modules: %}
include {{ puppet_module }}
{%- endfor %}
