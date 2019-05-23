package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strings"
	"log"
)

var (
	forLoop             = regexp.MustCompile(`^for\s?\(.*\)\s?{?$`)
	whileLoop           = regexp.MustCompile(`^while\s?\(.*\).*$`)
	ifStatement         = regexp.MustCompile(`^(}?\s?else\s?)?if\s?\(.*\).*$`)
	switchstatement     = regexp.MustCompile(`^switch\s?\(.*\).*$`)
	conditionaloperator = regexp.MustCompile(`^.*?.*:.*;`)
	functionCall        = regexp.MustCompile(`^.*\(.*\);$`)
	assignment          = regexp.MustCompile(`^.*(=.*|\+\+|\-\-);$`)
	returns             = regexp.MustCompile(`^return.*;$`)
	breakContinue       = regexp.MustCompile(`^(break|continue).*;$`)
	GoTo                = regexp.MustCompile(`^goto.*;$`)
)

func main() {
	if len(os.Args) < 2 {
		nbr := LLCs(os.Stdin)
		fmt.Println("LLCs: ", nbr)
	} else {
		for i := 2; i < len(os.Args); i++ {
			fp, err := os.Open(os.Args[i])
			if err != nil {
				log.Fatal(err)
			}
			fmt.Println(os.Args[i], ":", LLCs(fp))
		}
	}
}

func LLCs(fp *os.File) int {
	nbr := 0
	reader := bufio.NewReader(fp)
	for line, err := reader.ReadString('\n'); err == nil; line, err = reader.ReadString('\n') {
		bytes := []byte(strings.TrimSpace(line[:len(line)-1]))
		switch {
		case forLoop.Match(bytes) || whileLoop.Match(bytes) || GoTo.Match(bytes):
			nbr += 3
		case ifStatement.Match(bytes) || switchstatement.Match(bytes) || conditionaloperator.Match(bytes):
			nbr += 2
		case functionCall.Match(bytes) || assignment.Match(bytes) || returns.Match(bytes) || breakContinue.Match(bytes):
			nbr += 1
		default:
		}
	}
	return nbr
}
