import android.Keys._

android.Plugin.androidBuild

useProguard := false

name := "power-wlan"

scalaVersion := "2.11.3"

proguardCache in Android ++= Seq(
  ProguardCache("org.scaloid") % "org.scaloid"
)

proguardOptions in Android ++= Seq("-dontobfuscate", "-dontoptimize", "-keepattributes Signature"
  , "-dontwarn scala.collection.**" // required from Scala 2.11.3
  , "-dontwarn scala.collection.mutable.**" // required from Scala 2.11.0
)

libraryDependencies += "org.scaloid" %% "scaloid" % "3.6-10" withSources() withJavadoc()

libraryDependencies += "org.scalatest" % "scalatest_2.11" % "2.2.1" % "test"

scalacOptions in Compile += "-feature"

run <<= run in Android

install <<= install in Android

//debugIncludesTests := false

debugIncludesTests in Android := false