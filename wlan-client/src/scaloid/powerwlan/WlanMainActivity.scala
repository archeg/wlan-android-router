package scaloid.powerwlan

import org.scaloid.common._
import android.graphics.Color

class WlanMainActivity extends SActivity {

  onCreate {
    contentView = new SVerticalLayout {
      style {
        case t: STextView => t textSize 15.dip
      }


      STextView("Mac:")
      SEditText("")
      STextView("Ip address:")
      SEditText("")
	  this += new SLinearLayout {
	    STextView("Port: ")
      SEditText("9")
	  }.wrap
      SButton(R.string.red).onClick(wake)
    } padding 20.dip
  }

  def wake() = {
    toast("Bang!!!")
  }

}
