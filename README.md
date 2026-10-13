# Cyclizer Development Journal

Developer-only, **local-first** Cyclizer Plugin. Adds **Development Journal**
to Cyclizer's main navigation. Clicking it displays a native Cyclizer UI page
that reads Markdown directly from the running Cyclizer Host's own checked-out
`docs/plans` tree. The document index is lightweight; Markdown bodies are
read only when an article is selected.

## Strict privacy boundaries

- **No document contents, document copies, generated HTML or indexes** are
  included in this Plugin repository or its release ZIP.
- **No GitHub Pages, no HTTP server, no outgoing document requests, no public
  document publication.** Catalog hosting, if introduced later, is separate
  and contains only Plugin metadata.
- The Plugin process contributes only `cyclizer.ui-local-documents/v1` with
  `document_set: cyclizer.plans`. The trusted Cyclizer Host fixes that set
  to its own source `docs/plans`; the Plugin supplies no filesystem paths
  and receives no file bytes.
- Cyclizer's trusted UI displays local docs in its **main content area**, not
  in an external Browser Web Session. Markdown source is escaped before any
  restricted HTML formatting is applied; links only navigate to local listed
  Markdown documents.
- This is a read-only view. It does not copy files into a user profile.
- Development Journal 0.2.0 requires the Cyclizer Host with the
  `cyclizer.ui-local-documents/v1` contract. The old 0.1.0 external-link
  package is no longer the intended product.

## Source tree

```text
plugin/
  plugin.json
  components/third-party.development-journal/
    component.json
    process.py
scripts/build_plugin.py
tests/test_build_plugin.py
```

There is deliberately **no docs/plans directory or published journal
content** here.

## Build and test

```powershell
cd D:\Downloads\Workspace\cyclizer-plugin-development-journal
python scripts\build_plugin.py
python -m unittest discover -s tests -v
```

Output: `dist/packages/development-journal-0.2.0.cyclizer.plugin.zip`.
Install/update it through the existing Cyclizer **Settings → Plugins**
local ZIP workflow, restart the Host if package changes require it, and enable
the Component. The **Development Journal** menu item then opens an in-app
page with the local `docs/plans` repository documents.

The Host must be running from a checked-out Cyclizer source tree that still
contains `docs/plans`. A source-less installation displays a clear error
instead of downloading or substituting remote documentation.

The four Interaction kinds remain unchanged; this is another data-only
`Contribute` point, not an `Intercept` DOM-mutation ability.
