plugins {
    idea
    kotlin("jvm") version "1.8.21"
    id("io.papermc.paperweight.userdev") version "1.5.5"
}

java {
    toolchain.languageVersion.set(JavaLanguageVersion.of(17))
}

group = "com.example"


idea {
    module {
        excludeDirs.add(file(".server"))
    }
}

repositories {
    mavenCentral()
    maven("https://repo.papermc.io/repository/maven-public/")
}

dependencies {
    implementation(kotlin("stdlib"))
    compileOnly("io.papermc.paper:paper-api:1.19.4-R0.1-SNAPSHOT")
    paperDevBundle("1.19.3-R0.1-SNAPSHOT")
}

extra.apply {
    set("pluginName", project.name.split('-').joinToString("") { it.capitalize() })
    set("packageName", project.name.replace("-", ""))
    set("kotlinVersion", "1.8.21")
    set("paperVersion", "1.19.4")
}

tasks {
    processResources {
        filesMatching("*.yml") {
            expand(project.properties)
            expand(extra.properties)
        }
    }
    jar {
        archiveFileName.set(project.name + "-dev.jar")
        destinationDirectory.set(file(".server/plugins"))
    }
}
