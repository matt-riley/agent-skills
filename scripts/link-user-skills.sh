#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills_dir="$repo_root/skills"
ts="$(date +%Y%m%d-%H%M%S)"

link_dir() {
  local target="$1"
  local source="$2"
  mkdir -p "$(dirname "$target")"

  if [ -L "$target" ]; then
    rm "$target"
  elif [ -e "$target" ]; then
    mv "$target" "$target.pre-agent-skills-$ts"
  fi

  ln -s "$source" "$target"
  echo "linked $target -> $source"
}

link_dir "$HOME/.agents/skills" "$skills_dir"
link_dir "$HOME/.copilot/skills" "$skills_dir"
