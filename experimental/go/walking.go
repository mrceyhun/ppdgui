package main

import (
	"fmt"
	"go-hep.org/x/hep/groot/riofs"
	"go-hep.org/x/hep/groot/root"
	"log"
)

func main() {
	f, err := riofs.Open("../../dqm.root")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	//fmt.Printf("visit all ROOT file tree:\n")
	//err = riofs.Walk(f, func(path string, obj root.Object, err error) error {
	//    fmt.Printf("%s (%s)\n", path, obj.Class())
	//    return nil
	//})
	//if err != nil {
	//    log.Fatalf("could not walk through file: %v", err)
	//}

	obj, err := f.Get("DQMData")
	a := obj.(root.Object)
	if err != nil {
		log.Fatalf("could not walk through file: %v", err)
	}

	fmt.Println("visit only dir1:\n", obj)

}
