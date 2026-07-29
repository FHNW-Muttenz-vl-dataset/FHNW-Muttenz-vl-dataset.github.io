---
layout: default
title: Download
nav_order: 3
---

# Download

## License

This dataset is licensed under the [**Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**](https://creativecommons.org/licenses/by-nc/4.0/deed.en) license.

### You are free to:

**Share** — copy and redistribute the material in any medium or format\
**Adapt** — remix, transform, and build upon the material

### Under the following terms:

**Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made\
**NonCommercial** — You may not use the material for commercial purposes

## Access - download links

{: .note }
By downloading this dataset, you agree to the terms of the [License](#license).

| **Reference Data**    | [Download link](https://kdrive.infomaniak.com/app/share/1918313/e80814a5-47d4-44b9-baa5-83b693b2717c) |
| **Query Sequences**   | [Download link](https://kdrive.infomaniak.com/app/share/1918313/5884136c-ccbd-4d79-a16a-1629e109c249) |
{: .plain-table }

We provide the data bundled as zip-archive. The bundles are created per camera system for the reference data and per scene for the query sequences. Under the download link above you can select the bundles you would like to download. Please note that the size of the bundles varies greatly and the download may take some time.

### Checksums

Use these SHA-256 checksums to verify the completeness/integrity of a downloaded bundle. Click a checksum to copy it, or download the [full checksums manifest](assets/data/checksums.json) as JSON. You can compute a bundle's checksum yourself using [`scripts/compute_sha256.py`](https://github.com/FHNW-Muttenz-vl-dataset/FHNW-Muttenz-vl-dataset.github.io/blob/main/scripts/compute_sha256.py).

<style>
.checksum-table {
  border-collapse: collapse;
  width: 100%;
  table-layout: auto;
}
.checksum-table th, .checksum-table td {
  text-align: left;
  border: 0.25px solid #ccc;
  padding: 0.4em 0.75em;
  overflow-wrap: break-word;
}
.checksum-table code {
  font-size: 0.85em;
}
</style>

{% assign checksum_groups = site.data.checksums.bundles | group_by: "group" %}
{% for group in checksum_groups %}
#### {{ group.name }}

<table class="checksum-table">
  <thead>
    <tr><th>{% if group.name contains "Query" %}Scene{% else %}Camera system{% endif %}</th><th>File name</th><th>SHA-256 checksum</th></tr>
  </thead>
  <tbody>
    {% for bundle in group.items %}<tr><td>{{ bundle.label }}</td><td><code>{{ bundle.file }}</code> ({{ bundle.size_gb | default: "TODO" }} GB)</td><td><code class="copyable">{{ bundle.sha256 | default: "TODO" }}</code></td></tr>
    {% endfor %}
  </tbody>
</table>
{% endfor %}

## Privacy & anonymization

All personal data captured in the imagery of the FHNW Muttenz visual localization dataset has been completely anonymized. This goes beyond blurring faces and license plates: entire bodies and vehicles are blurred, ensuring that no personally identifiable content remains in the released images.
