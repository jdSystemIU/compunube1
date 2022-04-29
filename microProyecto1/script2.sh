#!/bin/bash
apt-get update

hname="$(hostname)" 

echo "Hello, my server name is $hname"
echo "Aprovisionando para VM3"
#Codigo para aprovisionar
echo "Establece una IP diferente para VM3"
#
sudo snap install lxd
sudo snap refresh lxd
#echo "\e[32mRemoving Old LXD if exists \e[0m"
#apt remove lxd lxd-client -y
#echo "\e[32mAdding non-root user to LXD Group \e[0m"
#usermod cloud_user -aG lxd

#Annadiendo a un grupo llamado lxd
sudo gpasswd -a vagrant lxd

#Guardamos el certificado en una variable local
certificate=$(</vagrant/servidor.crt)
echo "$certificate"

#evita sobreescribir en el mismo archivo, eliminandolo
rm lxdconfig.yaml

echo "\e[32mCreate Preseed File \e[0m"

cat >> lxdconfig.yaml << EOF
config: {}
networks: []
storage_pools: []
profiles: []
cluster:
  server_name: vagrantVM-3
  enabled: true
  member_config:
  - entity: storage-pool
    name: local
    key: source
    value: ""
    description: '"source" property for storage pool "local"'
  cluster_address: 172.16.16.101:8443
  cluster_certificate: |
$certificate
  server_address: 172.16.16.103:8443
  cluster_password: "admin"
  #cluster_certificate_path: ""
  #cluster_token: ""
EOF

  #cluster_certificate_path: "certificateServer.crt"
  #cluster_token: ""
echo "\e[32mInitialise LXD Using Preseed File \e[0m"
cat lxdconfig.yaml | lxd init --preseed

echo "\e[32mDone!! \e[0m"
lxc version
lxc cluster list


#----------------------------------Inicio aprovision APACHE
echo "Creando Contenedor web2"
lxc launch ubuntu:18.04 web2 < /dev/null
echo "Contenedor web1 creado"
sleep 15

#Se accede al contenedor web 1 y se actualiza el SO
sudo lxc exec web1 -- apt update -y
sudo lxc exec web1 -- apt upgrade -y
#Se instala apache en el contenedor web1
sudo lxc exec web2 -- apt-get install apache2 -y 
#Se reinicia apache en el contenedor web1
sudo lxc exec web2 -- systemctl restart apache2


echo "Configurar index.html"

#Se crea un archivo index.html para crear la pagina web 1
touch /home/vagrant/index.html
cat <<TEST> /home/vagrant/index.html
<!DOCTYPE html>
<html>
<body>
<h1>WEB 2</h1>
<p>Bienvenido al Web 2 del Miniproyecto de Computacion en la Nube</p>
</body>
</html>
TEST

lxc file push /home/vagrant/index.html web2/var/www/html/index.html

lxc exec web2 -- systemctl restart apache2

lxc config device add web2 http proxy listen=tcp:0.0.0.0:2080 connect=tcp:127.0.0.1:80
#--------------------- finalización APACHE------------------------------
#----------------------backup-----------------------------------------
sudo lxc launch ubuntu:18.04 web2backup < /dev/null
echo "Contenedor web2backup creado"

#Se accede al contenedor web 1 y se actualiza el SO
sudo lxc exec web2backup -- apt update -y
sudo lxc exec web2backup -- apt upgrade -y
#Se instala apache en el contenedor web1
sudo lxc exec web2backup -- apt-get install apache2 -y 
#Se reinicia apache en el contenedor web1
sudo lxc exec web2backup -- systemctl restart apache2


echo "Configurar index.html"

#Se crea un archivo index.html para crear la pagina web 1
touch /home/vagrant/index.html
cat <<TEST> /home/vagrant/index.html
<!DOCTYPE html>
<html>
<body>
<h1>WEB 2</h1>
<p>Bienvenido al Backup de WEB 2 - Computacion en la Nube</p>
</body>
</html>
TEST

lxc file push /home/vagrant/index.html web2backup/var/www/html/index.html

lxc exec web2backup -- systemctl restart apache2

lxc config device add web2backup http proxy listen=tcp:0.0.0.0:3080 connect=tcp:127.0.0.1:80
