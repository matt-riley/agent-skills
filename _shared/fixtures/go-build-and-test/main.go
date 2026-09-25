package main

import (
	"fmt"

	"example.com/gadget/greet"
)

func main() {
	retries := "3"
	fmt.Println(greet.Hello("world"))
	fmt.Println("attempts allowed:", retries+1)
}
