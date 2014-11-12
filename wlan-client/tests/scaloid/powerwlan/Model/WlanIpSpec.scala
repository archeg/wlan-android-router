package scaloid.powerwlan.Model

import scaloid.powerwlan.UnitSpec

/**
 * Created by archeg on 13.11.14.
 */
class WlanIpSpec extends UnitSpec {
  class NumberedIp(val numberOfTuples : Int, val tupleVal: Int = 2) {
    val ip = new WlanIp(0 until numberOfTuples map (x => tupleVal) mkString("."))
  }

  "An ip" should "accept 4 digits like 11.11.11.11" in new NumberedIp(4, 11) {
    ip should be ('validated)
  }

  it should "accept 1.23.46.254" in {
    val ip = new WlanIp("1.23.46.254")
    ip should be ('validated)

    val ipResult = ip.toBytes()
    ipResult should have size 4
    ipResult should be (Array(1, 23, 46, 254))
  }

  it should "not be validated if more than 4 items are given" in new NumberedIp(5, 11) {
    ip should not be ('validated)
  }

  it should "not accept be validated if less than 4 items are given" in new NumberedIp(3, 11) {
    ip should not be ('validated)
  }

  it should "not be validated if at least one number is bigger than 255" in {
    val ip = new WlanIp("1.23.256.1")
    ip should not be ('validated)
  }

  it should "not be validated if different symbols happen to present in ip" in {
    for (symbol <- Array('a', '?', '*', ',', ' ')) {
      val ip = new WlanIp("1.23.2" + symbol + ".1")
      ip should not be ('validated)
    }
  }
}
