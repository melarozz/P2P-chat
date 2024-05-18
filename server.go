package main

import (
    "bufio"
    "fmt"
    "net"
    "os"
    "strings"
)

func getEnv(key string, defaultVal string) string {
    if value, exists := os.LookupEnv(key); exists {
        return value
    }
    return defaultVal
}

func main() {
    var host = getEnv("HOST", "0.0.0.0")

    go startListener(host)
    fmt.Printf("Listener started at port 8080 on host %v\n", host)
    for {

    }
}

func startSender(conn *net.UDPConn) {
    for {
        host, message := inputMessage()
        if host == "all" {
            host = getBroadcastAddress()
        }
        sendMessage(host, message, conn)
    }
}

func sendMessage(addr string, message string, conn *net.UDPConn) {
    addr_, err := net.ResolveUDPAddr("udp", addr+":8080")
    if err != nil {
        panic(err)
    }
    _, err = conn.WriteTo([]byte(message), addr_)
    if err != nil {
        fmt.Printf("Couldn't send response %v", err)
    }
}

func inputMessage() (string, string) {
    fmt.Printf("Message: ")
    reader := bufio.NewReader(os.Stdin)
    input, _ := reader.ReadString('\n')
    var splitInput = strings.Split(input, " ")
    host, message := splitInput[0], splitInput[1]
    return host, message
}

func listen(ser *net.UDPConn, p []byte) {
    _, remote, err := ser.ReadFromUDP(p)
    fmt.Printf("New message from %v: %s", remote, p)
    if err != nil {
        fmt.Printf("Some error  %v", err)
    }
    fmt.Printf("Message: ")
}

func startListener(ip string) {
    p := make([]byte, 2048)
    addr := net.UDPAddr{
        Port: 8080,
        IP:   net.ParseIP(ip),
    }
    ser, err := net.ListenUDP("udp", &addr)
    if err != nil {
        fmt.Printf("Some error %v\n", err)
        return
    }
    go startSender(ser)
    for {
        listen(ser, p)
    }
}

func getBroadcastAddress() string {
    interfaces, err := net.Interfaces()
    if err != nil {
        panic(err)
    }

    for _, iface := range interfaces {
        if iface.Flags&net.FlagBroadcast != 0 {
            addrs, err := iface.Addrs()
            if err != nil {
                continue
            }
            for _, addr := range addrs {
                switch v := addr.(type) {
                case *net.IPNet:
                    if v.IP.To4() != nil {
                        // This is an IPv4 address
                        return v.IP.String()
                    }
                }
            }
        }
    }
    return "255.255.255.255" // Default to broadcast address
}
