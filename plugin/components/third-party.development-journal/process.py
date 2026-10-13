"""Local-only Development Journal contribution; no network or file operations."""

from cyclizer_plugin_sdk import LocalDocumentsPage, serve


def main() -> None:
    serve(
        "third-party.development-journal",
        local_documents=[
            LocalDocumentsPage(
                registration_id="development-journal",
                label="Development Journal",
                document_set="cyclizer.plans",
                order=30,
            )
        ],
    )


if __name__ == "__main__":
    main()
