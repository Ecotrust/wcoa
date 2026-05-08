FROM tomcat:9-jdk17

# ARG GEOPORTAL_VERSION=v265
# ARG GEOPORTAL_VERSION=v272
ARG GEOPORTAL_VERSION=v302

RUN rm -rf /usr/local/tomcat/webapps/*
COPY ./wars/geoportal.war $CATALINA_HOME/webapps/geoportal.war
COPY ./wars/harvester.war $CATALINA_HOME/webapps/harvester.war
# COPY ./wars/v265/geoportal.war $CATALINA_HOME/webapps/geoportal.war
# COPY ./wars/v265/harvester.war $CATALINA_HOME/webapps/harvester.war
# COPY ./wars/v272/geoportal.war $CATALINA_HOME/webapps/geoportal.war
# COPY ./wars/v272/harvester.war $CATALINA_HOME/webapps/harvester.war
# COPY ./wars/${GEOPORTAL_VERSION}/geoportal.war $CATALINA_HOME/webapps/geoportal.war
# COPY ./wars/gpcatalog/esri_geoportal_302.war $CATALINA_HOME/webapps/geoportal.war
# COPY ./wars/${GEOPORTAL_VERSION}/harvester.war $CATALINA_HOME/webapps/harvester.war

RUN echo es_node=elastic >> /usr/local/tomcat/conf/catalina.properties
RUN rm $CATALINA_HOME/conf/tomcat-users.xml
COPY ./files/tomcat-users.xml $CATALINA_HOME/conf/tomcat-users.xml
CMD ["catalina.sh", "run"]