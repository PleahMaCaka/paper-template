package example

import org.bukkit.plugin.java.JavaPlugin

class ExamplePlugin : JavaPlugin() {

    override fun onEnable() {
        logger.info("Example Plugin Enable!")
    }

    override fun onDisable() {

    }

}