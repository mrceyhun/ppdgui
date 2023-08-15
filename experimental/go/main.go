package main

import (
	"fmt"
	"go-hep.org/x/hep/groot"
	"go-hep.org/x/hep/groot/rhist"
	"go-hep.org/x/hep/groot/riofs"
	"log"
	"strings"
)

func findObj(filePath, objPath string) any {
	var obj any
	f, err := groot.Open(filePath)
	if err != nil {
		log.Fatal(err)
	}
	defer func(f *groot.File) {
		err := f.Close()
		if err != nil {
			log.Println("ROOT file could not close successfully!")
		}
	}(f)

	// Get object path list by separating by slash
	pathList := strings.Split(objPath, "/")
	obj, err = f.Get(pathList[0])
	if err != nil {
		log.Fatal(err)
	}

	for _, objDir := range pathList[1:] {
		obj, err = obj.(riofs.Directory).Get(objDir)
		if err != nil {
			log.Fatal(err)
		}
	}
	return obj
}

func main() {
	//f, err := groot.Open("../../dqm.root")
	//if err != nil {
	//	log.Fatal(err)
	//}
	//
	//defer f.Close()
	//a, err := f.Get("DQMData")
	//b, err := a.(riofs.Directory).Get("Run 366713").(riofs.Directory).Get("EcalPreshower")
	//if err != nil {
	//	log.Fatal(err)
	//}
	//fmt.Printf("entries= %v\n", b)

	//keys := f.Keys()
	//for _, k := range keys {
	//	fmt.Printf("entries= %v\n", k.)
	//}
	a := findObj("../../dqm.root", "DQMData/Run 366713/EcalPreshower/Run summary/ESRecoSummary/recHits_ES_energyMax")
	f := a.(rhist.H1)
	fmt.Printf("name= %v\n", f)
}
