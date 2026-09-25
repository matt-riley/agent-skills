package main

import "fmt"

// version is injected at build time by goreleaser ldflags.
var version = "dev"

func main() {
	fmt.Println("rel", version)
}
