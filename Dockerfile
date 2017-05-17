FROM autodeskls/ochopod:1.0.7_20161220203100CET
ADD /pod /opt/flaskChatbot/pod
ADD resources/supervisor /etc/supervisor/conf.d
WORKDIR /opt/flaskChatbot
EXPOSE 80
CMD /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf