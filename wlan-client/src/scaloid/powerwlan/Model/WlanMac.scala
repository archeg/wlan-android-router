package scaloid.powerwlan.Model

/**
 * Created by archeg on 10.11.14.
 */
class WlanMac(mac: String) {
    val pattern = "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$".r

    private def toHex(s: String) = Integer.parseInt(s, 16)

    def toBytes() = {
        mac split "[:-]" map toHex
    }

    def validated() = {
        mac match {
            case pattern(_*) => true
            case _ => false
        }
    }
}
