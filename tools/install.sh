main() {
  # Use colors, but only if connected to a terminal, and that terminal
  # supports them.
  if which tput >/dev/null 2>&1; then
      ncolors=$(tput colors)
  fi
  if [ -t 1 ] && [ -n "$ncolors" ] && [ "$ncolors" -ge 8 ]; then
    RED="$(tput setaf 1)"
    GREEN="$(tput setaf 2)"
    YELLOW="$(tput setaf 3)"
    BLUE="$(tput setaf 4)"
    BOLD="$(tput bold)"
    NORMAL="$(tput sgr0)"
  else
    RED=""
    GREEN=""
    YELLOW=""
    BLUE=""
    BOLD=""
    NORMAL=""
  fi

  # Only enable exit-on-error after the non-critical colorization stuff,
  # which may fail on systems lacking tput or terminfo
  set -e

  # Prevent the cloned repository from having insecure permissions. Failing to do
  # so causes compinit() calls to fail with "command not found: compdef" errors
  # for users with insecure umasks (e.g., "002", allowing group writability). Note
  # that this will be ignored under Cygwin by default, as Windows ACLs take
  # precedence over umasks except for filesystems mounted with option "noacl".
  umask g-w,o-w

  printf "${BLUE}Cloning Kubeb...${NORMAL}\n"
  command -v git >/dev/null 2>&1 || {
    echo "Error: git is not installed"
    exit 1
  }

  if [ ! -n "$KUBEB" ]; then
    KUBEB=~/.kubeb
  fi

  if [ -d "$KUBEB" ]; then
    printf "${YELLOW}You already have Kubeb installed.${NORMAL}\n"
    printf "You'll need to remove $KUBEB if you want to re-install.\n"
    exit
  fi
  
  env git clone --depth=1 https://github.com/tuantranf/kubeb.git "$KUBEB" || {
    printf "Error: git clone of Kubeb repo failed\n"
    exit 1
  }

  printf "${BLUE}Installing the Kubeb to ${KUBEB}${NORMAL}\n"
  ORIGIN_DIR="$PWD"

  cd "$KUBEB" || {
    printf "Error: change to Kubeb directory failed\n"
    exit 1
  }

  command -v python3 >/dev/null 2>&1 || {
    echo "Error: python3 is not installed"
    exit 1
  }

  python3 -m venv .env3
  source .env3/bin/activate
  pip install -r requirements.txt
  pip install --editable .

  cd "$ORIGIN_DIR"

  printf "${GREEN}"
  echo 'Kubeb ....is now installed.'
  echo 'Happy Kubeb!'
}

main
