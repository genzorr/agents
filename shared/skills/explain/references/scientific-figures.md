# Scientific figures

Use this reference for scientific figures that communicate measured results, including interpretation of an existing figure. For interpretation, identify what the figure and its sources establish and what remains unknown; do not regenerate it or require unavailable source data merely to explain its visible content. For creation, use the project's existing analysis and plotting path with standard plotting tools. This reference owns presentation and evidence checks, not statistical estimators, experiment design, or permission to collect more data.

## Preserve the evidence

- Bind plotted values to identifiable data or run artifacts and retain the generating script, input references, transformations, and regeneration command in the project's existing output structure. Distinguish measured, derived, fitted, and illustrative values; synthetic examples must be visibly identified and must not become reported results.
- Choose the comparison axis from the claim. Steps compare work only when work per step is comparable; a speed claim needs elapsed time and relevant hardware context. Confirm units from the data rather than relabelling a step column as tokens, frames, or seconds without a supported conversion.
- Preserve the unit of replication, run/seed identities and actual counts. State what an interval describes and how it was computed. Use the project's approved analysis for paired or independent comparisons; an effect claim needs uncertainty of the difference, not an inference from overlap of separate intervals. A single run does not establish between-run uncertainty. Missing replication is a limitation to report, not authorization to launch runs.
- Disclose smoothing, interpolation, normalization, exclusions and stopped runs. For trajectory aggregation, avoid extrapolated tails beyond observed support; state the common range and show materially different run behavior rather than hiding it in a mean. Missing or failed measurements remain distinct from poor valid values.
- A trade-off comparison must identify settings, seed variation and search budgets. Do not silently make the best individual seed the frontier representative; use the project's declared setting-level summary or explicitly label an exploratory run-level frontier. Connecting measured points does not establish attainable intermediate performance. Distinguish a fit and its extrapolation from measurements, and retain the fit's selected points and limitations.

## Choose the visual by the question

| Question | Representation and fidelity check |
|---|---|
| How does a metric change over a run? | Curves on a comparable axis; distinguish raw observations from smoothing and show the available run variation. |
| What changed relative to a baseline? | A difference plot with a zero reference and the analysis-defined uncertainty; preserve direction and units. Bars that encode magnitude by length need a meaningful zero baseline. |
| What performance is traded for cost? | A scatter or frontier with direction of improvement, dominated observations where relevant, and comparable budgets or an explicit limitation. |
| What pattern appears across a measurement grid? | Shared normalization for panels being compared; a zero-centered diverging scale for signed changes; label the colorbar and distinguish missing cells. Use positions or a table when exact small differences are the question. |
| What does a reconstruction or image comparison reveal? | Genuine raster panels with comparable views, scales and disclosed crops. Preserve qualitative counterexamples; vector export of axes does not make image pixels vector data. |

Use redundant labels, markers or line styles when color alone would obscure a comparison in grayscale or for a colorblind reader. Do not impose a fixed palette, seed count, panel count, fit family or chart-size threshold independently of the question and data.

## Publication output

For a paper or an explicitly requested publication export, derive dimensions from the actual document or venue template and lay out at that final size. Rescaling a large canvas can make its text unreadable; cropping on export can also change the physical dimensions. Reflow labels and panels before shrinking the whole figure. Prefer vector output for plots and text when the destination supports it; retain raster content for images and use the requested supported format.

Write the caption with the figure: a claim supported by the visible evidence plus the units, replication, uncertainty definition and transformations needed to interpret it. State material omissions. Use panel labels and comparable scales for related panels. In a paper, avoid an axes title that merely repeats the caption; a standalone chart may need its own title.

Inspect the exported artifact at its intended display or print size, not only the source canvas. Check clipping, label collisions, font rendering, legibility, legend mappings, units and comparable axes/color scales. A file-save success or automated layout check does not establish evidence validity. Fix detectable defects before delivery and state any inspection or toolchain limitation. Deliver usable links to the figure and its reproducibility source under the host's and project's existing conventions.

## Provenance

Mechanisms re-authored from [alphaXiv/OpenResearch orx-figures](https://github.com/alphaXiv/OpenResearch/tree/db0ca91d0c77f122220bb398888db763e6d69bef/agent-skills/orx-figures), reviewed 2026-09-07 (MIT). No upstream code or templates are included. Its application-specific commands, artifact roots, statistics helpers and fixed publication defaults are not dependencies of this reference.
