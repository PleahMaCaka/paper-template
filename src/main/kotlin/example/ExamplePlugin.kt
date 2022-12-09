package example

import org.bukkit.plugin.java.JavaPlugin

class ExamplePlugin : JavaPlugin() {

    companion object {
        lateinit var instance: ExamplePlugin
            private set
    }

    override fun onEnable() {
        logger.info("Example Plugin Enable!")
    }

    override fun onDisable() {

    }

}