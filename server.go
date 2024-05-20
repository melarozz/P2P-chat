package main

import (
  "bufio"
  "fmt"
  "net"
  "os"
  "strings"
)

func getEnv(key string, value string) string {
  if value, exists := os.LookupEnv(key); exists {
    return value
  }

  return value
}

func main() {
  var host = getEnv("HOST", "0.0.0.0")

  go startListen(host)
  fmt.Printf("Listener started at port 8080 on host %v\n", host)
}

func startSender(conn *net.UDPConn) {
  for {
    host, message := inputMessage()
    if host == "all" {
      host = "255.255.255.255"
      message = "(for all) " + message
    }
    sendMessage(host, message, conn)
  }
}

func sendMessage(addr string, message string, conn *net.UDPConn) {
  addr_, err := net.ResolveUDPAddr("udp", addr+":8080")
  _, err = conn.WriteTo([]byte(message), addr_)
}

func inputMessage() (string, string) {
  fmt.Printf("Enter message: ")
  reader := bufio.NewReader(os.Stdin)
  input, _ := reader.ReadString('\n')
  var splitInput = strings.SplitN(input, " ", 2)
  host, message := splitInput[0], splitInput[1]
  return host, message
}

func listen(ser *net.UDPConn, p []byte) {
  _, remote, err := ser.ReadFromUDP(p)
  fmt.Printf("New message from %v: %s", remote, p)
  fmt.Printf("Enter message: ")
}

func startListen(ip string) {
  p := make([]byte, 2048)
  addr := net.UDPAddr{
    Port: 8080,
    IP:   net.ParseIP(ip),
  }
  ser, err := net.ListenUDP("udp", &addr)
  go startSender(ser)
  for {
    listen(ser, p)
  }
}
