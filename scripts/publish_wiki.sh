#!/usr/bin/env bash
set -euo pipefail

# Publica o conteúdo da pasta ./wiki para a GitHub Wiki do repositório.
# Uso:
#   scripts/publish_wiki.sh <owner/repo> [https|ssh]
# Exemplo:
#   scripts/publish_wiki.sh rodrigobprado/Home-Security-DIY https

REPO_SLUG="${1:-}"
PROTO="${2:-https}"

if [[ -z "$REPO_SLUG" ]]; then
  echo "Uso: $0 <owner/repo> [https|ssh]"
  exit 1
fi

if [[ ! -d "wiki" ]]; then
  echo "Pasta wiki/ não encontrada no diretório atual."
  exit 1
fi

case "$PROTO" in
  https)
    WIKI_URL="https://github.com/${REPO_SLUG}.wiki.git"
    ;;
  ssh)
    WIKI_URL="git@github.com:${REPO_SLUG}.wiki.git"
    ;;
  *)
    echo "Protocolo inválido: $PROTO (use https ou ssh)"
    exit 1
    ;;
esac

WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

echo "Clonando wiki: $WIKI_URL"
git clone "$WIKI_URL" "$WORKDIR/wiki-repo"

rsync -av --delete --exclude '.git' wiki/ "$WORKDIR/wiki-repo/"

pushd "$WORKDIR/wiki-repo" >/dev/null
if [[ -n "$(git status --porcelain)" ]]; then
  git add .
  git commit -m "docs: atualiza wiki do projeto"
  git push origin master || git push origin main
  echo "Wiki publicada com sucesso."
else
  echo "Sem alterações para publicar."
fi
popd >/dev/null
