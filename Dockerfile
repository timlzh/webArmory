FROM httpd:alpine3.18

COPY site /usr/local/apache2/htdocs/

EXPOSE 80