(defproject kafka-gps-client "0.0.1-SNAPSHOT"
  :source-paths ["src/clj"]
  :java-source-paths ["src/main"]
  :resource-paths ["multilang"]
  :aot :all
  :repositories {
                 "akka" "http://repo.typesafe.com/typesafe/releases/",
                 "local" ~(str (.toURI (java.io.File. "maven_repository")))
                 }

  :dependencies [
                   ;; [org.clojure/clojure-contrib "1.2.0"]
                   ;; [log4j/log4j "1.2.16"]
                   ;; [org.jsoup/jsoup "1.6.1"]
                   ;; [com.gravity/goose "2.1.22"]
                   [commons-collections/commons-collections "3.2.1"]
                   [storm/storm-kafka "0.8.0-wip4"]
                   [zookeeper-clj "0.9.3"]
                 ]

  :profiles {:dev
              {:dependencies [[storm "0.8.2"]]}}
  :min-lein-version "2.0.0"
  )
