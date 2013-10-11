.PHONY: uwsgi /usr/sbin/nginx

build: /usr/bin/git /usr/sbin/nginx /usr/include/python2.7/import.h src/uwsgi/uwsgi
	echo "make done"

/usr/include/python2.7/import.h: # python-dev
	apt-get -y install python-dev python-requests

/usr/bin/git:
	apt-get -y install git

/usr/sbin/nginx:
	apt-get -y install nginx
	ln -sf /vagrant/nginx-site.conf /etc/nginx/sites-enabled/default
	/etc/init.d/nginx start

clean:
	apt-get -y remove nginx git python-dev
	apt-get -y autoremove
	rm -rf src/uwsgi


src/uwsgi:
	mkdir -p src
	git clone https://github.com/unbit/uwsgi.git src/uwsgi

src/uwsgi/uwsgi: src/uwsgi
	@make -C src/uwsgi
