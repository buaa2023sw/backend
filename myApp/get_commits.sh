echo '['
git rev-list HEAD | while read sha1; do
    full_diff="$(git show --format='' $sha1 | sed 's/\"/\\\"/g' | awk '{printf "%s\\n", $0}')"
    git --no-pager show --format="{%n  \"commithash\": \"%H\",%n  \"author\": \"%an\",%n \"authorEmail\": \"%ae\",%n  \"commitTime\": \"%ad\",%n  \"commitMessage\": \"%s\"%n}," -s $sha1
    done
echo ']'
