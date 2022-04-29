#!/bin/bash
apt-get update

#instalacion de apache
#lxc exec web1 -- apt-get install apache2

hname="$(hostname)" 
echo "Hello, my server name is $hname"
echo "Aprovisionando para haproxy"
#Codigo para aprovisionar haproxy
echo "Establece una IP diferente para VM1"
echo "\e[32mInstalling LXD Using Snap \e[0m"

sudo snap install lxd
sudo snap refresh lxd

#echo "\e[32mRemoving Old LXD if exists \e[0m"
#apt remove lxd lxd-client -y
#echo "\e[32mAdding non-root user to LXD Group \e[0m"
#usermod cloud_user -aG lxd

#Annadiendo a un grupo llamado lxd
sudo gpasswd -a vagrant lxd


#evita sobreescribir en el mismo archivo, eliminandolo
rm lxdconfig.yaml

echo "\e[32mCreate Preseed File \e[0m"
cat >> lxdconfig.yaml << EOF
config:
  core.https_address: 172.16.16.101:8443
  core.trust_password: admin
networks:
- config:
    bridge.mode: fan
    fan.underlay_subnet: auto
  description: ""
  name: lxdfan0
  type: ""
storage_pools:
- config: {}
  description: ""
  name: local
  driver: dir
profiles:
- config: {}
  description: ""
  devices:
    eth0:
      name: eth0
      network: lxdfan0
      type: nic
    root:
      path: /
      pool: local
      type: disk
  name: default
cluster:
  server_name: vagrantVM-1
  enabled: true
  member_config: []
  cluster_address: ""
  cluster_certificate: ""
  server_address: ""
  cluster_password: ""
  cluster_certificate_path: ""
  cluster_token: ""
EOF


echo "\e[32mInitialise LXD Using Preseed File \e[0m"
cat lxdconfig.yaml | lxd init --preseed

echo "\e[32mDone!! \e[0m"
lxc version
lxc cluster list  

######
sudo cp /var/snap/lxd/common/lxd/cluster.crt /vagrant/cluster.crt
sed 's/^/   /g' /vagrant/cluster.crt > /vagrant/servidor.crt

#-------------------------------HAPROXY----------------------
sudo lxc launch ubuntu:18.04 haproxy < /dev/null


sudo lxc exec haproxy -- apt update && apt upgrade -y
sudo lxc exec haproxy -- apt install haproxy -y

sudo lxc exec haproxy -- systemctl enable haproxy

echo "Configurando Archivo de Configuración Haproxy"

rm haproxy.cfg
#Se crea el archivo que va a tener la configuracion del balanceador de carga.
touch /home/vagrant/haproxy.cfg

cat <<TEST> /home/vagrant/haproxy.cfg
global
  log /dev/log  local0
  log /dev/log  local1 notice
  chroot /var/lib/haproxy
  stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
  stats timeout 30s
  user haproxy
  group haproxy
  daemon

  # Default SSL material locations
  ca-base /etc/ssl/certs
  crt-base /etc/ssl/private

  # Default ciphers to use on SSL-enabled listening sockets.
  # For more information, see ciphers(1SSL). This list is from:
  #  https://hynek.me/articles/hardening-your-web-servers-ssl-ciphers/
  # An alternative list with additional directives can be obtained from
  #  https://mozilla.github.io/server-side-tls/ssl-config-generator/?server=haproxy
  ssl-default-bind-ciphers ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:RSA+AESGCM:RSA+AES:!aNULL:!MD5:!DSS
  ssl-default-bind-options no-sslv3

defaults
  log global
  mode  http
  option  httplog
  option  dontlognull
        timeout connect 5000
        timeout client  50000
        timeout server  50000
  errorfile 400 /etc/haproxy/errors/400.http
  errorfile 403 /etc/haproxy/errors/403.http
  errorfile 408 /etc/haproxy/errors/408.http
  errorfile 500 /etc/haproxy/errors/500.http
  errorfile 502 /etc/haproxy/errors/502.http
  errorfile 503 /etc/haproxy/errors/503.http
  errorfile 504 /etc/haproxy/errors/504.http


backend web-backend
   balance roundrobin
   stats enable
   stats auth admin:admin
   stats uri /haproxy?stats

   option allbackups
   server web1 172.16.16.102:2080 check
   server web2 172.16.16.103:2080 check
   server web1backup 172.16.16.102:3080 check backup
   server web2backup 172.16.16.103:3080 check backup



frontend http
  bind *:80
  default_backend web-backend

TEST

lxc file push haproxy.cfg haproxy/etc/haproxy/haproxy.cfg


lxc exec haproxy -- systemctl start haproxy

lxc config device add haproxy http proxy listen=tcp:0.0.0.0:1080 connect=tcp:127.0.0.1:80

lxc exec haproxy -- systemctl restart haproxy

echo "Configurar index.html Para manejar Errores de fallas en los Servidores"

touch /home/vagrant/503.html
cat <<TEST> /home/vagrant/503.html
HTTP/1.0 503 Service Unavailable
Cache-Control: no-cache
Connection: close
Content-Type: text/html

<html>
<body>
<h1>ERROR OCURRIDO</h1>
<p>Error en la pagina. Estamos trabajando para ofrecer el mejor servicio </p>
</body>
</html>
TEST

lxc file push /home/vagrant/503.html haproxy/etc/haproxy/errors/503.http


lxc exec haproxy -- systemctl restart haproxy
#...........................finaliza HAPROXY.................