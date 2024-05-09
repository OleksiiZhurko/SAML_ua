FROM openjdk:17-jdk-alpine

WORKDIR /app

COPY . /app/

RUN chmod +x ./gradlew
RUN ./gradlew clean build -x test
RUN mv build/libs/MLHandler.jar App.jar

ENTRYPOINT ["java", "-jar", "App.jar"]
