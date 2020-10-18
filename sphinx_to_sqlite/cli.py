import click
import copy
import pathlib
import sqlite_utils
from xml.etree import ElementTree as ET


@click.command()
@click.version_option()
@click.argument("db_path", type=click.Path(file_okay=True, dir_okay=False))
@click.argument(
    "build_dir", type=click.Path(file_okay=False, dir_okay=True, exists=True)
)
def cli(db_path, build_dir):
    "Load .xml files from build directory into SQLite"
    root = pathlib.Path(build_dir)
    paths = list(root.glob("*.xml"))
    found = []
    for path in paths:
        et = ET.fromstring(path.read_text())
        for section in et.findall("section"):
            find_sections_recursive(section, path.stem, found)
    db = sqlite_utils.Database(db_path)
    db["sections"].insert_all(found, pk="id", replace=True)
    db["sections"].enable_fts(
        ["title", "content"], tokenize="porter", create_triggers=True
    )


def find_sections_recursive(section, page, append_to, breadcrumbs=None):
    breadcrumbs = breadcrumbs or []
    title = section.find("title").text
    section_copy = copy.deepcopy(section)
    # Remove all child sections
    for child in section_copy.findall("section"):
        section_copy.remove(child)
    # and the title
    section_copy.remove(section_copy.find("title"))
    content = "".join(section_copy.itertext()).strip()
    ref = section.attrib["ids"].split()[-1]
    append_to.append(
        {
            "id": "{}:{}".format(page, ref),
            "page": page,
            "ref": ref,
            "title": title,
            "content": content,
            "breadcrumbs": breadcrumbs,
            "references": [
                {"href": ref.attrib["refuri"], "label": ref.text}
                for ref in section_copy.findall(".//reference")
                if "refuri" in ref.attrib and ref.attrib.get("internal") != "True"
            ],
        }
    )
    for child in section.findall("section"):
        find_sections_recursive(child, page, append_to, breadcrumbs + [title])
