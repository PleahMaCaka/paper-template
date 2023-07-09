val kotlinVersion = "1.9.0"
val javaVersion = 17

val paperVersion = "1.20.1"

group = "io.github.pleahmacaka"
version = "0.1.0"

plugins {
    val kotlinVersion = "1.9.0"
    idea
    kotlin("jvm") version kotlinVersion
    id("io.papermc.paperweight.userdev") version "1.5.3"
}

repositories {
    mavenCentral()
}

dependencies {
    implementation(kotlin("stdlib"))
    implementation(kotlin("reflect"))
    paperweight.paperDevBundle("$paperVersion-R0.1-SNAPSHOT")
}

extra.apply {
    set("pluginName", project.name.split('-').joinToString(""))
    set("packageName", project.name.replace('-', '.'))
    set("pluginVersion", version)
    set("kotlinVersion", kotlinVersion)
    set("paperVersion", paperVersion)
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

    withType<JavaCompile>().configureEach {
        if (javaVersion >= 10 || JavaVersion.current().isJava10Compatible) {
            options.release.set(javaVersion)
        }
    }

    processResources {
        val props = mapOf("version" to version)
        inputs.properties(props)
        filteringCharset = "UTF-8"
        filesMatching("paper-plugin.yml") {
            expand(props)
        }
    }
}

idea {
    module {
        excludeDirs.add(file(".server"))
    }
}

kotlin {
    jvmToolchain(javaVersion)
}

java {
    val javaVersion = JavaVersion.toVersion(javaVersion)

    sourceCompatibility = javaVersion
    targetCompatibility = javaVersion
    if (JavaVersion.current() < javaVersion)
        toolchain.languageVersion.set(JavaLanguageVersion.of(this@Build_gradle.javaVersion))

    toolchain {
        languageVersion.set(JavaLanguageVersion.of(17))
    }
}