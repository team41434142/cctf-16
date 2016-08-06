package main

import (
	"bufio"
	"crypto/sha256"
	"fmt"
	"os"
	"io"
)

func main() {
	f, err := os.Open("rockyou.txt")
	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		h256 := sha256.New()
		text := scanner.Text()
		io.WriteString(h256, text)
		fmt.Printf("%x: %s\n", h256.Sum(nil), text)
	}
}
