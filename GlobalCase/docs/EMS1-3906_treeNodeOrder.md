# EMS1-3906 Tree Node order

## Purpose

Verify that every sibling group in the Map tree is displayed in the required node order.

## Marker

`@pytest.mark.Unicase`

## Steps

1. Log in to EMS Web and open **Map**.
2. Show the navigation tree if it is hidden.
3. Expand every available Submap recursively.
4. Read only the direct child Submap nodes (the globe-icon nodes) under the root and under every expanded Submap.
5. Verify each sibling group independently using this priority:
   special characters, `0-9`, `a-z`, `A-Z`, Chinese characters.

## Expected result

- All reachable Submaps are expanded and checked.
- Submap nodes at every level match the required display order.
- A mismatch reports the parent node, actual order, and expected order.

## Notes

- Only direct children of the same parent are compared. Descendant text is not included in the parent group.
- Device nodes are excluded from the ordering data and are not expanded; line cards and other device descendants are not checked.
- `EMS` is the fixed tree root and is excluded from the sortable Submap list.
- English names use case-insensitive dictionary order; lowercase precedes uppercase only when the remaining comparison is identical.
- The check does not create, rename, move, or delete any Map node.
