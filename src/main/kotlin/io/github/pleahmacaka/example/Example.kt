package io.github.pleahmacaka.example

import org.bukkit.plugin.java.JavaPlugin

@Suppress("unused")
class Example : JavaPlugin() {

    companion object {
        lateinit var instance: Example
            private set
    }

    override fun onEnable() {
        instance = this
        logger.info("Example Plugin Enabled!")
    }

    override fun onDisable() {
        logger.info("Example Plugin Disabled!")
    }

}
