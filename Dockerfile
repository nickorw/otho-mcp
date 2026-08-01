# Stage 1: Java runtime
FROM eclipse-temurin:25-jre-noble AS java-base

# Stage 2: Get OOPs WAR from published image
FROM mpovedavillalon/oops:v2 AS oops-source

# Stage 3: Final image — Python + Java + Tomcat + OOPs
FROM python:3.11-slim-bookworm

# Copy Java from stage 1
COPY --from=java-base /opt/java/openjdk /opt/java/openjdk
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Install Tomcat + curl
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
ENV CATALINA_HOME=/opt/tomcat
RUN mkdir -p $CATALINA_HOME && \
    curl -fsSL https://archive.apache.org/dist/tomcat/tomcat-9/v9.0.118/bin/apache-tomcat-9.0.118.tar.gz | \
    tar xz --strip-components=1 -C $CATALINA_HOME && \
    rm -rf $CATALINA_HOME/webapps/*

# Copy OOPs WAR from stage 2
COPY --from=oops-source /usr/local/tomcat/webapps/OOPS.war $CATALINA_HOME/webapps/OOPS.war

# Add JAXB libs for Java 11+ compatibility (OOPs was built for Java 7/8)
RUN curl -fsSL -o $CATALINA_HOME/lib/jaxb-api-2.3.1.jar \
      https://repo1.maven.org/maven2/javax/xml/bind/jaxb-api/2.3.1/jaxb-api-2.3.1.jar && \
    curl -fsSL -o $CATALINA_HOME/lib/jaxb-impl-2.3.3.jar \
      https://repo1.maven.org/maven2/com/sun/xml/bind/jaxb-impl/2.3.3/jaxb-impl-2.3.3.jar && \
    curl -fsSL -o $CATALINA_HOME/lib/jaxb-core-2.3.0.1.jar \
      https://repo1.maven.org/maven2/com/sun/xml/bind/jaxb-core/2.3.0.1/jaxb-core-2.3.0.1.jar && \
    curl -fsSL -o $CATALINA_HOME/lib/javax.activation-1.2.0.jar \
      https://repo1.maven.org/maven2/com/sun/activation/javax.activation/1.2.0/javax.activation-1.2.0.jar

WORKDIR /app

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy application
COPY src/ src/
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
