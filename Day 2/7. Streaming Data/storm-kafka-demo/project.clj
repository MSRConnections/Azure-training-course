(defproject storm-kafka-gps-example "0.0.1-SNAPSHOT"
  :java-source-paths ["src/main"]
  :resource-paths ["resources" "resources/commons-lang3-3.1.jar" "resources/commons-logging-1.1.1.jar" "resources/jackson-core-asl-1.9.2.jar" "resources/jackson-jaxrs-1.9.2.jar" "resources/jackson-mapper-asl-1.9.2.jar" "resources/jackson-xc-1.9.2.jar" "resources/javax.inject-1.jar" "resources/jaxb-impl-2.2.3-1.jar" "resources/jaxb-impl-2.2.3-1-sources.jar" "resources/jersey-client-1.13.jar" "resources/jersey-client-1.13-sources.jar" "resources/jersey-core-1.13.jar" "resources/jersey-core-1.13-sources.jar" "resources/jersey-json-1.13.jar" "resources/jersey-json-1.13-sources.jar" "resources/jettison-1.1.jar" "resources/mail-1.4.5.jar" "resources/mail-1.4.5-sources.jar" "resources/microsoft-windowsazure-api-0.4.6.jar" "resources/dom4j-1.6.jar" "resources/jaxen-1.1.1.jar"]
  :aot :all
  :repositories {
                 ;;"twitter4j" "http://twitter4j.org/maven2"
                 "akka" "http://repo.typesafe.com/typesafe/releases/",
                 "local" ~(str (.toURI (java.io.File. "maven_repository")))
                 }

  :dependencies [
                   [org.clojure/clojure "1.5.0-alpha3"]
                   [org.clojure/clojure-contrib "1.2.0"]
                   ;;[org.twitter4j/twitter4j-core "3.0.3"]
                   ;;[org.twitter4j/twitter4j-stream "3.0.3"]
                   [log4j/log4j "1.2.16"]
                   [redis.clients/jedis "2.0.0"]
                   [org.jsoup/jsoup "1.6.1"]
                   [com.gravity/goose "2.1.22"]
                   [commons-collections/commons-collections "3.2.1"]
                   [storm/storm "0.8.2"]
                   [storm/storm-kafka "0.8.0-wip4"]
                   [com.vividsolutions/jts "1.8"]
                   [org.json/json "20080701"]
                 ]

  :profiles {:dev
              {:dependencies [[storm "0.8.2"]]}}
                              
  :min-lein-version "2.0.0"
  )
