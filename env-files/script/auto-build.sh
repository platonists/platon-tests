# init
WORK_DIR="/home/shing/build-pips"
CACHE_DIR="${WORK_DIR}/newpackage"
CODE_DIR="/home/shing/github/platon-network/PlatON-Go"
VERSION_FILE="${CODE_DIR}/params/version.go"
BIN_FILE='platon'
TAR_FILE="platon-pips.tar.gz"


# get current version
Major_Version=`sed -n 's/.*VersionMajor = \(\S\)/\1/p' ${VERSION_FILE} | awk '{print $1}'`
Minor_Version=`sed -n 's/.*VersionMinor = \(\S\)/\1/p' ${VERSION_FILE} | awk '{print $1}'`
Patch_Version=`sed -n 's/.*VersionPatch = \(\S\)/\1/p' ${VERSION_FILE} | awk '{print $1}'`
Current_Version="${Major_Version}.${Major_Version}.${Major_Version}"


# set target version
version1="${Major_Version}.6.1"
version2="${Major_Version}.${Minor_Version}.0"
version3="${Major_Version}.${Minor_Version}.9"
version4="${Major_Version}.$((${Minor_Version}+1)).0"
version5="${Major_Version}.$((${Minor_Version}+1)).1"
version6="${Major_Version}.$((${Minor_Version}+1)).9"
version7="${Major_Version}.$((${Minor_Version}+2)).0"
version8="9.7.1"
version9="8.7.1"
version_names=("version1" "version2" "version3" "version4" "version5" "version6" "version7" "version8" "version9")


# print target versions
print_versions() {
  echo -e "current version: ${Current_Version} \n"
  cd ${CODE_DIR}
  for version_name in "${version_names[@]}"
  do
    version_str=${!version_name}
    version_seq=(${version_str//./ })
    version_number=$((${version_seq[0]} * 65536 + ${version_seq[1]} * 256 + ${version_seq[2]}))
    echo "${version_name}: ${version_str}  ${version_number}"
  done
}


# build target versions
build_versions(){
  cd ${CODE_DIR}
  for version_name in "${version_names[@]}"
  do
    version_str=${!version_name}
    version_seq=(${version_str//./ })
    echo -e "\n\n # BUILD VERSION ${version_str}... \n\n"
    sed -i "s/VersionMajor = ${Major_Version}/VersionMajor = ${version_seq[0]}/" ${VERSION_FILE}
    sed -i "s/VersionMinor = ${Minor_Version}/VersionMinor = ${version_seq[1]}/" ${VERSION_FILE}
    sed -i "s/VersionPatch = ${Patch_Version}/VersionPatch = ${version_seq[2]}/" ${VERSION_FILE}
    make clean && make platon
    save_dir="${CACHE_DIR}/${version_name}"
    mkdir -p ${save_dir} && mv "${CODE_DIR}/build/bin/platon" "${save_dir}"
    git checkout ${VERSION_FILE}
  done
  mv "${CACHE_DIR}/version5/platon" "${CACHE_DIR}"
}


# tar target versions
tar_versions() {
	cd ${WORK_DIR}
	tar -czvf ${TAR_FILE} "./newpackage"
}


# clear target versions
clear_versions() {
	rm -rf ${CACHE_DIR}
	rm -rf ${WORK_DIR}/${TAR_FILE}
}


####
## main program
####

# Defining 'versions' command
versions() {
	print_versions
}

# Defining 'build' command
build() {
	clear_versions
	build_versions
	tar_versions
}


# run main
command=$1
[ -z ${command} ] && command='versions'
echo -e "\n ---------------- \n"
${command}
echo -e "\n ---------------- \n"
