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
	. "github.com/sbwhitecap/tqdm/iterators"
)

const LISTFILE_PREFIX = "songlist-"
const LISTFILE_SUFFIX = ".json"
const SUFFIX_HOSTNAME bool = true
const TARGET_FILE_PATTERN = ".mp3"

func LogErr(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

func Info(texts ...string) {
	fmt.Println("| [Info]", strings.Join(texts, " "))
}
func Warn(texts ...string) {
	fmt.Println("| [Warn]", strings.Join(texts, " "))
}
func Pause() {
	fmt.Print("Press enter to continue ...")
	var in string
	fmt.Scanln(&in)
}

func get_old_list_files(base_dir string) []string {
	var list_files []string
	files, err := ioutil.ReadDir(base_dir)
	LogErr(err)
	for _, f := range files {
		if (strings.HasPrefix(f.Name(), LISTFILE_PREFIX) && filepath.Ext(f.Name()) == LISTFILE_SUFFIX) {
			list_files = append(list_files, f.Name())
		}
	}
	return list_files
}

func read_old_list_file(base_dir string) map[string]uint32 {
	fmt.Println("* __ READ OLD LIST FILES ______")
	defer fmt.Println("`")
	var old_list_file string
	if len(os.Args) > 1 {
		Info("Input file:", os.Args[1])
		old_list_file = filepath.Join(base_dir, os.Args[1])
	} else {
		old_list_files := get_old_list_files(base_dir)
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

func generate_new_list(base_dir string) map[string]uint32 {
	fmt.Println("* __ GENERATE NEW LIST ______")
	defer fmt.Println("`")
	now := time.Now().Format("20060102_150405")
	file_hashes := make(map[string]uint32)
	Info("Target files pattern:", TARGET_FILE_PATTERN)
	var pathlist []string
	err := filepath.Walk(base_dir, func(fpath string, finfo os.FileInfo, err error) error {
		if filepath.Ext(fpath) == TARGET_FILE_PATTERN {
			pathlist = append(pathlist, fpath)
		}
		return nil
	})
	LogErr(err)
	tqdm.With(Strings(pathlist), "", func(val interface{}) (brk bool) {
		fpath := val.(string)
		fbytes, err := ioutil.ReadFile(fpath)
		LogErr(err)
		file_hashes[filepath.Base(fpath)] = crc32.ChecksumIEEE(fbytes)
		return
	})
	hostname_badge := ""
	if SUFFIX_HOSTNAME {
		hostname, err := os.Hostname()
		LogErr(err)
		hostname_badge = "-" + strings.ReplaceAll(hostname, "-", "")
	}
	new_list_filename := LISTFILE_PREFIX + now + hostname_badge + LISTFILE_SUFFIX
	fpath := filepath.Join(base_dir, new_list_filename)
	json_bytes, json_err := json.MarshalIndent(file_hashes, "", "    ")
	LogErr(json_err)
	write_err := ioutil.WriteFile(fpath, json_bytes, 0644)
	LogErr(write_err)
	Info("New list file generated:", new_list_filename)
	return file_hashes
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
	BASE_DIR, _ := os.Getwd()
	Info("BASE_DIR:", BASE_DIR)
	old_list := read_old_list_file(BASE_DIR)
	new_list := generate_new_list(BASE_DIR)
	if len(old_list) > 0 && len(new_list) > 0 {
		diffs := dict_diffs(old_list, new_list)
		if len(diffs) > 0 {
			Info("Changes since last time:")
			for name, _ := range diffs {
				fmt.Println(name)
			}
		} else {
			Info("No changes")
		}
	} else {
		Info("Done")
	}
	Pause()
}
