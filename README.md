# fontPens

A collection of classes implementing the pen protocol for manipulating glyph outlines.

## Maintainers: how to release

To cut a release, make an annotated git tag, where the tag is in this format:
v1.2.3, where 1, 2 and 3 represent major, minor and micro version numbers.
You can add "aN" or "bN" or "rc" to mark alpha, beta or "release candidate"
versions. Examples: v1.2.3, v1.2.3b2, v1.2.3a4, v1.2.3rc.

The message for the annotated tag should contain the release notes.

Then use "git push --follow-tags" to trigger the release bot. Example session:

- `$ git tag -a v1.2.3 -m "v1.2.3 -- fixed issue #12345"`
- `$ git push --follow-tags`

This process will create a GitHub release, as well as upload the package to
PyPI.
