package scaloid.powerwlan.Model

/**
 * Created by archeg on 13.11.14.
 */
class WlanIp(ip: String) {
  val pattern = "^(([0-9]{1,3})\\.){3}([0-9]{1,3})".r

  private def toByte(s: String) = s.getBytes()(0)

  def toBytes() = {
    ip split "\\." map toByte
  }

  def validated() = {
    val ipSplitted = ip split "\\." map Integer.parseInt
    val isProperValue = ipSplitted forall (x => x < 255)
    ip match {
      case pattern(_*) => ipSplitted.size == 4 && isProperValue
      case _ => false
    }
  }
}
