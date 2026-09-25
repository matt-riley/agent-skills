package greet

import "testing"

func TestHello(t *testing.T) {
	if got, want := Hello("Ada"), "Hello, Ada"; got != want {
		t.Fatalf("Hello(Ada) = %q, want %q", got, want)
	}
}
