(
  set -e

  case "$(uname -m)" in
    x86_64) ARCH=amd64 ;;
    aarch64) ARCH=arm64 ;;
    *) echo "Unsupported architecture: $(uname -m)"; exit 1 ;;
  esac

  RELEASE_URL=$(curl -fsSL -o /dev/null -w '%{url_effective}' \
    https://github.com/cli/cli/releases/latest)

  VERSION="${RELEASE_URL##*/}"
  VERSION="${VERSION#v}"

  WORKDIR=$(mktemp -d)
  trap 'rm -rf "$WORKDIR"' EXIT

  curl -fL \
    "https://github.com/cli/cli/releases/download/v${VERSION}/gh_${VERSION}_linux_${ARCH}.tar.gz" \
    -o "$WORKDIR/gh.tar.gz"

  tar -xzf "$WORKDIR/gh.tar.gz" -C "$WORKDIR"

  sudo install -m 0755 \
    "$WORKDIR/gh_${VERSION}_linux_${ARCH}/bin/gh" \
    /usr/local/bin/gh

  /usr/local/bin/gh --version
)
