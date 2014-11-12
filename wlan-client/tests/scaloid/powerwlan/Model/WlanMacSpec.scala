package scaloid.powerwlan.Model

import org.scalatest.FlatSpec
import scaloid.powerwlan.UnitSpec

/**
 * Created by archeg on 12.11.14.
 */
class WlanMacSpec extends UnitSpec {
  class NumberedMac(var numberOfTuples : Int, var tupleSize: Int = 2) {
    val mac = new WlanMac(0 until numberOfTuples map (x => "1" * tupleSize) mkString("-"))
  }

  "A mac" should "accept six two-number tuples" in new NumberedMac(6) {
    mac.validated() should be (true)
  }

  it should "not accept more than six two-number tuples" in new NumberedMac(7){
    mac shouldNot be ('validated)
  }

  it should "not accept less than six two-number tuples" in new NumberedMac(5) {
    mac shouldNot be ('validated)
  }

  it should "not accept if tuple is more than two symbols" in new NumberedMac(6, 3) {
    mac shouldNot be ('validated)
  }

  it should "not accept if tuple is less than two symbols" in new NumberedMac(6, 1) {
    mac shouldNot be ('validated)
  }

  it should "return parsed values if given six '11' tuples" in new NumberedMac(6, 2){
    all (mac.toBytes()) shouldBe 0x11
  }

  it should "be parsed if complicated mac is passed" in {
    val mac = new WlanMac("e0:3f:49:a0:1d:eb")
    val macResult = mac.toBytes()

    mac shouldBe 'validated
    macResult should have size 6
    macResult should be (Array(0xe0, 0x3f, 0x49, 0xa0, 0x1d, 0xeb))
  }

  it should "not be validated if at least one tuple is bigger than 2" in {
    val mac = new WlanMac("e0:3f:49:a0s:1d:eb")
    mac shouldNot be ('validated)
  }

  it should "not be validated if at least one tuple is lesser than 2" in {
    val mac = new WlanMac("e0:3f:49:a:1d:eb")
    mac shouldNot be ('validated)
  }

  it should "not be validated if at least one letter is not hex" in {
    val mac = new WlanMac("e0:3f:49:ag:1d:eb")
    mac shouldNot be ('validated)
  }
}
