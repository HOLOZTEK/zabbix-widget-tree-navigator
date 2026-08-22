#!/bin/sh
set -eu

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <version>" >&2
    echo "Example: $0 1.4.12" >&2
    exit 2
fi

version="$1"
tag="v${version}"
repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

fail() {
    echo "ERROR: $*" >&2
    exit 1
}

manifest_version=$(jq -r '.version' "$repo_root/manifest.json")
[ "$manifest_version" = "$version" ] || fail "manifest.json version is $manifest_version, expected $version"

rpm_version=$(awk '/^Version:/ {print $2; exit}' "$repo_root/packaging/rpm/zabbix-widget-tree-navigator.spec")
[ "$rpm_version" = "$version" ] || fail "RPM spec version is $rpm_version, expected $version"

deb_version=$(dpkg-parsechangelog -l "$repo_root/debian/changelog" -S Version 2>/dev/null || true)
[ "$deb_version" = "$version" ] || fail "Debian changelog version is $deb_version, expected $version"

for readme in README.md README.ja.md; do
    path="$repo_root/$readme"
    grep -q "releases/tag/${tag}" "$path" || fail "$readme is missing releases/tag/${tag}"
    grep -q "releases/download/${tag}/zabbix-widget-tree-navigator-${version}.noarch.rpm" "$path" || fail "$readme RPM URL does not match $version"
    grep -q "releases/download/${tag}/zabbix-widget-tree-navigator_${version}_all.deb" "$path" || fail "$readme DEB URL does not match $version"
    grep -q "releases/download/${tag}/zabbix-widget-tree-navigator-${version}.tar.gz" "$path" || fail "$readme source URL does not match $version"
    grep -q "zabbix-widget-tree-navigator-${version}.noarch.rpm" "$path" || fail "$readme RPM install command does not match $version"
    grep -q "zabbix-widget-tree-navigator_${version}_all.deb" "$path" || fail "$readme DEB install command does not match $version"
    grep -q "zabbix-widget-tree-navigator-${version}.tar.gz" "$path" || fail "$readme source archive command does not match $version"
done

echo "Release version check passed: $version"
