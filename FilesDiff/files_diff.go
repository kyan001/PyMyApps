package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"encoding/json"
	"io/ioutil"
	"time"
	"strings"
	"hash/crc32"
	"github.com/sbwhitecap/tqdm"
	"github.com/sbwhitecap/tqdm/iterators"
)

const version = "1.5.1"

var BASE_DIR, dir_err = os.Getwd()
var HOSTNAME, host_err = os.Hostname()

const TARGET_FILE_PATTERN = ".mp3"
var LISTFILE_PREFIX = TARGET_FILE_PATTERN[1:] + "list-"
const LISTFILE_SUFFIX = ".json"
const HASH_MODE = "CRC32"  // "CRC32", "MTIME"
const SEPARATE_HOST bool = true


func LogErr(err error) {
	if err != nil {
		log.Fatal(err)
	}
}


func Info(texts ...string) {
	fmt.Println("| (Info)", strings.Join(texts, " "))
}


func Warn(texts ...string) {
	fmt.Println("| (Warn)", strings.Join(texts, " "))
}


func Pause() {
	fmt.Print("Press Enter to Continue...")
	var press_enter string
	fmt.Scanln(&press_enter)
}

func get_old_list_files() []string {
	var list_files []string
	files, err := ioutil.ReadDir(BASE_DIR)
	LogErr(err)
	for _, f := range files {
		if (strings.HasPrefix(f.Name(), LISTFILE_PREFIX) && filepath.Ext(f.Name()) == LISTFILE_SUFFIX) {
			if (SEPARATE_HOST && !strings.Contains(f.Name(), HOSTNAME)) {
				continue
			}
			list_files = append(list_files, f.Name())
		}
	}
	return list_files
}


func read_old_list_file() map[string]uint32 {
	fmt.Println("* __ READ OLD LIST FILES ______")
	defer fmt.Println("`")
	var old_list_file string
	if len(os.Args) > 1 {
		input_file := filepath.Base(os.Args[1])
		old_list_file = filepath.Join(BASE_DIR, input_file)
		Info("Input file:", input_file)
	} else {
		old_list_files := get_old_list_files()
		if len(old_list_files) > 0 {
			old_list_file = old_list_files[len(old_list_files)-1]
		} else {
			old_list_file = ""
		}
	}
	if old_list_file == "" {
		Warn("Old list file does not found, ignored.")
	} else {
		Info("Old list file:", old_list_file)
		json_bytes, err := ioutil.ReadFile(old_list_file)
		LogErr(err)
		var old_list map[string]uint32
		unmarshal_err := json.Unmarshal(json_bytes, &old_list)
		LogErr(unmarshal_err)
		Info(fmt.Sprint(len(old_list)), "entries loaded")
		return old_list
	}
	return nil
}


func generate_new_list() map[string]uint32 {
	fmt.Println("* __ GENERATE NEW LIST ______")
	defer fmt.Println("`")
	file_hashes := make(map[string]uint32)
	Info("Target files pattern:", TARGET_FILE_PATTERN)
	var pathlist []string
	err := filepath.Walk(BASE_DIR, func(fpath string, finfo os.FileInfo, err error) error {
		if filepath.Ext(fpath) == TARGET_FILE_PATTERN {
			pathlist = append(pathlist, fpath)
		}
		return nil
	})
	LogErr(err)
	tqdm.With(iterators.Strings(pathlist), "", func(val interface{}) (brk bool) {
		fpath := val.(string)
		fbytes, err := ioutil.ReadFile(fpath)
		LogErr(err)
		var fhash uint32
		if HASH_MODE == "CRC32" {
			fhash = crc32.ChecksumIEEE(fbytes)
		} else if HASH_MODE == "MTIME" {
			f, ferr := os.Open(fpath)
			LogErr(ferr)
			fi, fierr := f.Stat()
			LogErr(fierr)
			fhash = uint32(fi.ModTime().Unix())
		} else {
			fhash = 0
		}
		file_hashes[filepath.Base(fpath)] = fhash
		return
	})
	return file_hashes
}


func save_new_list(new_list map[string]uint32) {
	fmt.Println("* __ SAVE NEW LIST ______")
	defer fmt.Println("`")
	now := time.Now().Format("20060102_150405")
	hostname_badge := ""
	if SEPARATE_HOST {
		hostname_badge = "-" + HOSTNAME
	}
	new_list_filename := LISTFILE_PREFIX + now + hostname_badge + LISTFILE_SUFFIX
	fpath := filepath.Join(BASE_DIR, new_list_filename)
	json_bytes, json_err := json.MarshalIndent(new_list, "", "    ")
	LogErr(json_err)
	write_err := ioutil.WriteFile(fpath, json_bytes, 0644)
	LogErr(write_err)
	Info("New list file generated:", new_list_filename)
}


func dict_diffs(dict1 map[string]uint32, dict2 map[string]uint32) map[string]uint32 {
	diffs := make(map[string]uint32)
	for name, hash := range dict1 {
		if val, is_exist := diffs[name]; is_exist {
			if val == hash {
				delete(diffs, name)
			}
		} else {
			diffs[name] = hash
		}
	}
	for name, hash := range dict2 {
		if val, is_exist := diffs[name]; is_exist {
			if val == hash {
				delete(diffs, name)
			}
		} else {
			diffs[name] = hash
		}
	}
	return diffs
}


func main() {
	Info("Version:", version)
	LogErr(dir_err)
	Info("BASE_DIR:", BASE_DIR)
	LogErr(host_err)
	Info("HOSTNAME:", HOSTNAME)
	old_list := read_old_list_file()
	new_list := generate_new_list()
	if len(old_list) > 0 && len(new_list) > 0 {
		diffs := dict_diffs(old_list, new_list)
		if len(diffs) > 0 {
			Info("Changes since last time:")
			for name, _ := range diffs {
				fmt.Println(name)
			}
			save_new_list(new_list)
		} else {
			Info("No changes")
		}
	} else {
		save_new_list(new_list)
		Info("Done")
	}
	Pause()
}
