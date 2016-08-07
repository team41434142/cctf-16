package main

import (
	"bufio"
	"bytes"
	"crypto/sha256"
	"encoding/base64"
	"errors"
	"fmt"
	"io"
	"os"
	"strings"
)

func brute(salt string, encodedHash string) (string, error) {
	f, err := os.Open("rockyou.txt")
	if err != nil {
		return "", err
	}

	hash, err := base64.StdEncoding.DecodeString(encodedHash)
	if err != nil {
		return "", err
	}

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		h256 := sha256.New()
		text := scanner.Text()
		io.WriteString(h256, text + salt)

		if bytes.Equal(hash, h256.Sum(nil)) {
			return text, nil
		}
	}

	return "", errors.New("Failed")
}

func main() {
	f, err := os.Open("hashes.txt")
	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		split := strings.Split(scanner.Text(), "$")

		result, err := brute(split[1], split[2])
		if err == nil {
			fmt.Printf("%s\n", result)
		}/* else {
			fmt.Printf("error: %v\n", err)
		}*/
	}
}
