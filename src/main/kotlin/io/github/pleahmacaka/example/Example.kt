package io.github.pleahmacaka.example

import org.bukkit.plugin.java.JavaPlugin

@Suppress("unused")
class Example : JavaPlugin() {

    companion object {
        lateinit var instance: Example
            private set
    }

    override fun onEnable() {
        logger.info("Example Plugin Enabled!")
    }

    override fun onDisable() {

    }

}
