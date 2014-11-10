package scaloid.powerwlan

import java.net.{DatagramSocket, InetAddress, DatagramPacket}

/**
 * Created by archeg on 10.11.14.
 */
class WlanPacketSender(mac: Array[Byte], ip: Array[Byte], port: Int = 9) {

    def send() = {
        val address = InetAddress getByAddress ip


        // TODO: Not a Scala way?
        val bytes = new Array[Byte](102)
        for(i <- 0 until 6){
           bytes(i) = 0xFF.asInstanceOf[Byte]
        }

        for(i <- 6 until bytes.length){
            System.arraycopy(mac, 0, bytes, i, mac.length)
        }

        val packet = new DatagramPacket(bytes, bytes.length, address, port)
        val socket = new DatagramSocket()
        socket.send(packet)
        socket.close()
    }
}
