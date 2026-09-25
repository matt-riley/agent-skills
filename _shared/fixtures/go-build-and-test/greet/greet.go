package greet

import "fmt"

// Hello returns a greeting for name.
func Hello(name string) string {
	return fmt.Sprintf("Hi, %s", name)
}
