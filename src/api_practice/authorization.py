# ================================================================
# H1 | Deny precedence
# ================================================================
# Question:
# Implement effective_permissions(roles, mapping, denied).
# Combine grants from all roles. Unknown roles grant nothing.
# Remove every denied permission, then return unique permissions
# sorted alphabetically. The role order must not change the answer.


def effective_permissions(roles, mapping, denied):
    """Return the user's final permissions as a sorted list.

    roles: A list of role names.
    mapping: A dictionary mapping known roles to permission lists.
    denied: A list of explicitly denied permissions.
    """
    # I use a set because I only need one copy of each permission.
    permissions = set()

    for role in roles:
        if role in mapping:
            # I add the permissions for this role, not the role name.
            permissions.update(mapping[role])
        # An unknown role adds nothing. It does not erase earlier grants.

    # I remove denials last so another role cannot add them back.
    permissions.difference_update(denied)

    # I return a list with a predictable alphabetical order.
    return sorted(permissions)


def test_effective_permissions():
    """Check the supplied example and the required edge cases."""
    mapping = {
        "reader": ["read"],
        "editor": ["read", "write"],
    }
    duplicate_mapping = {
        "reader": ["read", "read"],
        "editor": ["read", "write", "write"],
    }
    unsorted_mapping = {"admin": ["write", "read", "delete"]}

    # Each case contains: roles, mapping, denied, expected result.
    cases = [
        # Supplied example and reversed role order.
        (["reader", "editor"], mapping, ["write"], ["read"]),
        (["editor", "reader"], mapping, ["write"], ["read"]),
        # Duplicate roles, duplicate permissions, and both together.
        (["reader", "reader", "editor"], mapping, [], ["read", "write"]),
        (["reader", "editor"], duplicate_mapping, [], ["read", "write"]),
        (["editor", "editor"], duplicate_mapping, ["write"], ["read"]),
        # Unknown roles alone and mixed with known roles.
        (["unknown"], mapping, [], []),
        (["reader", "unknown", "editor"], mapping, ["write"], ["read"]),
        # All grants denied.
        (["reader", "editor"], mapping, ["read", "write"], []),
        # No roles, no denials, and a denial that was never granted.
        ([], mapping, [], []),
        (["reader", "editor"], mapping, [], ["read", "write"]),
        (["reader", "editor"], mapping, ["delete"], ["read", "write"]),
        # Repeated denials and denying a different permission.
        (["reader", "editor"], mapping, ["write", "write"], ["read"]),
        (["reader", "editor"], mapping, ["read"], ["write"]),
        # A single role and an empty mapping.
        (["editor"], mapping, [], ["read", "write"]),
        (["reader"], {}, ["delete"], []),
        # The output must be sorted, not kept in the input order.
        (["admin"], unsorted_mapping, [], ["delete", "read", "write"]),
    ]

    for roles, test_mapping, denied, expected in cases:
        actual = effective_permissions(roles, test_mapping, denied)
        assert actual == expected, (
            f"H1 failed: roles={roles!r}, mapping={test_mapping!r}, "
            f"denied={denied!r}; expected {expected!r}, got {actual!r}"
        )

    return len(cases)


# ================================================================
# H2 | Return the first validation error
# ================================================================
# Question:
# Implement name_error(text), assuming text is a string.
# A valid name is 3-8 characters long, starts with a-z, and uses
# only ASCII lowercase letters a-z, digits 0-9, or underscores.
# Check the original input. Do not trim spaces or lowercase it.
#
# Return the first applicable error in this exact order:
# 1. "length" if the length is outside 3-8.
# 2. "start" if the first character is not a-z.
# 3. "character:i" for the first forbidden character's index.
# 4. "" if the name is valid.
# The index starts at 0. Return the result; do not just print it.


def name_error(text):
    """Return the first error string, or an empty string if valid."""
    # I check length first, before trying to access text[0].
    if not (3 <= len(text) <= 8):
        return "length"

    # The first character must be an ASCII lowercase letter.
    if not (text[0] <= "z" and text[0] >= "a"):
        return "start"

    for i, char in enumerate(text):
        letter = "a" <= char <= "z"
        digit = "0" <= char <= "9"

        # I return immediately when I find the first forbidden character.
        if not (letter or digit or char == "_"):
            return f"character:{i}"

    # I reach this only if every check passes.
    return ""


def test_name_error():
    """Check valid names, boundaries, character rules, and priority."""
    # Each case contains: original input, expected result.
    cases = [
        ("abc", ""),                  # Valid; exactly 3 characters.
        ("a_1", ""),                  # Letters, underscore, and digit.
        ("ab", "length"),             # Supplied example; too short.
        ("1ab", "start"),             # Supplied example; digit first.
        ("ab-", "character:2"),       # Supplied example; hyphen at 2.
        ("a__", ""),                  # Repeated underscores are allowed.
        ("abcdefgh", ""),             # Exactly 8 characters.
        ("abcdefghi", "length"),      # 9 characters: too long.
        ("ABC", "start"),             # Uppercase first character.
        ("aBc", "character:1"),       # Uppercase later in the name.
        ("abC", "character:2"),       # Uppercase at the last index.
        ("A", "length"),              # Length wins over start.
        ("1-", "length"),             # Length wins over multiple errors.
        ("1-b", "start"),             # Start wins over the later hyphen.
        ("A-b", "start"),             # Start still has higher priority.
        ("a-!", "character:1"),       # Report the first forbidden index.
        ("ab!?", "character:2"),      # Report 2, not the later error at 3.
        ("", "length"),               # Empty input does not crash.
        ("a", "length"),              # One character is too short.
        ("_ab", "start"),             # An underscore cannot come first.
        ("abc_", ""),                 # A trailing underscore is allowed.
        ("a1234567", ""),             # Valid 8-character name with digits.
        ("a12345678", "length"),      # Same pattern, but too long.
        (" abc", "start"),            # Do not trim a leading space.
        ("abc ", "character:3"),      # Do not trim a trailing space.
        ("a b", "character:1"),       # A space inside is forbidden.
        ("a\tb", "character:1"),      # A tab is forbidden.
        ("ab\n", "character:2"),      # A newline is forbidden.
        ("éab", "start"),             # Non-ASCII letter at the start.
        ("aéb", "character:1"),       # Non-ASCII letter later.
        ("a١b", "character:1"),       # Arabic-Indic digit is not ASCII.
        ("a１b", "character:1"),      # Fullwidth digit is not ASCII.
    ]

    for text, expected in cases:
        actual = name_error(text)
        assert actual == expected, (
            f"H2 failed: text={text!r}; "
            f"expected {expected!r}, got {actual!r}"
        )

    return len(cases)


# ================================================================
# H3 | Explain the consequence
# ================================================================

# 1. Why apply denial after all grants?
# My answer:
# If I remove a permission before I finish adding all the grants,
# another role could give that permission back. I apply denials last
# so the denied permissions stay removed in the final answer.

# 2. Why is an unknown role not admin?
# My answer:
# I do not know what permissions an unknown role should have, so I
# should not guess or give it admin access. It contributes nothing.
# This does not remove permissions from the user's other known roles.

# 3. Why is length checked first?
# My answer:
# If the string is empty, accessing text[0] would cause an IndexError.
# I check length first to avoid that. The question also says that
# a length error must come before a start or character error.

# 4. Why not silently lowercase the input?
# My answer:
# If I lowercase the input first, uppercase letters could pass after
# I change them. I need to check the original input, not fix it first.

# 5. Is a logged-in user automatically allowed to delete?
# My answer:
# No. Logging in only verifies who the user is. The user still needs
# permission to delete, and an explicit denial wins in this exercise.
# A read-only user cannot delete. Write permission does not necessarily
# include delete permission either; those can be separate permissions.


# ================================================================
# Submission notes | Complexity
# ================================================================

# H1 input-size variables:
# r = number of entries in roles, including repeated roles.
# p = total permission entries visited across those roles,
#     including repeated permissions and repeated visits.
# d = number of entries in denied.
# u = number of unique permissions collected before removing denials.
#
# H1 time complexity: average O(r + p + d + u log u).
# My explanation:
# I visit r roles. Checking whether a role is in the dictionary is
# O(1) on average, so I do not scan the whole mapping for every role.
# update() still processes each permission in that role's list.
# Across all roles, that adds O(p) average work, not just O(r).
# I then process d denials. Finally, I sort the remaining permissions.
# There are at most u left, so O(u log u) is a sorting upper bound.
# I assume short, fixed-size strings and average dictionary/set lookups.
#
# H1 extra-space complexity: O(u).
# My explanation:
# I store up to u unique permissions in a new set. The sorted output
# also needs up to u entries. Two linear amounts still give O(u).
# Even if every grant is denied, I stored the grants before removing
# them, so I count that peak memory use, not only the final output.

# H2 input-size variable:
# n = number of characters in text.
#
# H2 time complexity:
# O(n) describes the general character-scanning approach.
# O(1) is the tighter bound for this exact fixed 3-8-character rule.
# My explanation:
# The length and first-character checks take constant time.
# A general scan checks up to n characters, so that is O(n).
# However, this function rejects lengths outside 3-8 before the loop.
# It never scans more than 8 characters, even for a very long input.
# With this fixed limit and a normal Python string, its time is O(1).
#
# H2 extra-space complexity: O(1).
# My explanation:
# I do not build another list or set. I only keep the current index,
# character, and a few temporary values. Under this fixed length rule,
# the returned error string also has a bounded size.



# ================================================================
# Run all tests
# ================================================================

if __name__ == "__main__":
    h1_count = test_effective_permissions()
    h2_count = test_name_error()

    print(f"H1: {h1_count} tests passed.")
    print(f"H2: {h2_count} tests passed.")
    print("All tests passed.")
