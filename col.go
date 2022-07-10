package main

import (
	"fmt"
	"io/ioutil"
)

const version = "0.0.1"

func main() {
	fmt.Println("Goer v", version)
}

func getFile(filename string) string {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Println(err)
		content = nil
	}
	return string(content)
}
