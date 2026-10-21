# Spec Delta

## MODIFIED Requirements

### Requirement: Each plugin has one state
Each plugin SHALL have exactly one state: `candidate`, `default`, `opt-in` or `archived`.
Exactly one plugin SHALL have the state `default`.

- `candidate`: under evaluation. Offered for installation.
- `default`: the plugin a project uses unless it chooses another. Offered for installation.
- `opt-in`: kept for use on request. Offered for installation.
- `archived`: deprecated and kept for reference. Not offered for installation.

#### Scenario: Initial states
- **WHEN** a plugin is added to the catalog
- **THEN** its state is `candidate`, and the state of the default plugin is unchanged
