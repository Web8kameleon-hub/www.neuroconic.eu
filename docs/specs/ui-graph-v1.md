# UI Graph Spec v1

Specifikim i saktë për modelin e grafit të UI për `ui-composer` dhe profilet në `personal_node`.

## Scope

- **Producer**: `UIDesignEngine.generate_schema`, `attach_plugin_to_schema`.
- **Consumer**: frontend renderer (`ui_composer*.html`, dashboard UI).
- **Version**: `ui_graph_version = "1.0"`.

## Canonical Graph Model

```json
{
  "ui_graph_version": "1.0",
  "profile_id": "default",
  "owner_id": "local-user",
  "nodes": [
    {
      "id": "widget_welcome",
      "type": "widget",
      "widget_type": "hero",
      "title": "Welcome Creator",
      "props": { "subtitle": "Design your personal UI node" },
      "position": { "col": 1, "row": 1, "w": 12, "h": 1 },
      "status": "active"
    }
  ],
  "edges": [
    {
      "id": "edge_refresh_welcome",
      "from": "action_refresh",
      "to": "widget_welcome",
      "type": "triggers",
      "condition": "always"
    }
  ],
  "integrations": {
    "plugins": [],
    "nodedb_fluid": { "enabled": true, "storage": "local-device" },
    "tide": { "enabled": true, "mode": "batica-zbatica" }
  },
  "meta": {
    "created_at": "2026-09-02T19:40:00Z",
    "updated_at": "2026-09-02T19:40:00Z",
    "schema_hash": "sha256:..."
  }
}
```

## Node Types

- `widget`: element i vizueshëm (`hero`, `status`, `timeline`, `console`, `markdown`, etj.)
- `action`: event/command (`refresh`, `save_layout`, `api_call`)
- `data_source`: endpoint/binding (`/api/health`, `/api/lightning/stats`)
- `integration`: plugin connector i validuar

## Edge Types

- `triggers`: `action -> widget|data_source`
- `feeds`: `data_source -> widget`
- `binds`: `integration -> widget|data_source`
- `depends_on`: rend ekzekutimi

## JSON Schema (Validation)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://www.neurosonic.eu/specs/ui-graph-v1.schema.json",
  "title": "NeurosonicUiGraphV1",
  "type": "object",
  "additionalProperties": false,
  "required": ["ui_graph_version", "profile_id", "nodes", "edges", "meta"],
  "properties": {
    "ui_graph_version": { "const": "1.0" },
    "profile_id": { "type": "string", "minLength": 1, "maxLength": 128 },
    "owner_id": { "type": "string", "minLength": 1, "maxLength": 64 },
    "nodes": {
      "type": "array",
      "minItems": 1,
      "maxItems": 500,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["id", "type", "status"],
        "properties": {
          "id": { "type": "string", "pattern": "^[a-zA-Z0-9_.:-]{3,80}$" },
          "type": { "type": "string", "enum": ["widget", "action", "data_source", "integration"] },
          "widget_type": { "type": "string", "minLength": 1, "maxLength": 64 },
          "title": { "type": "string", "maxLength": 180 },
          "props": { "type": "object" },
          "position": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
              "col": { "type": "integer", "minimum": 1, "maximum": 24 },
              "row": { "type": "integer", "minimum": 1, "maximum": 500 },
              "w": { "type": "integer", "minimum": 1, "maximum": 24 },
              "h": { "type": "integer", "minimum": 1, "maximum": 500 }
            }
          },
          "status": { "type": "string", "enum": ["active", "disabled", "hidden"] }
        }
      }
    },
    "edges": {
      "type": "array",
      "maxItems": 1500,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["id", "from", "to", "type"],
        "properties": {
          "id": { "type": "string", "pattern": "^[a-zA-Z0-9_.:-]{3,100}$" },
          "from": { "type": "string" },
          "to": { "type": "string" },
          "type": { "type": "string", "enum": ["triggers", "feeds", "binds", "depends_on"] },
          "condition": { "type": "string", "maxLength": 200 }
        }
      }
    },
    "integrations": { "type": "object" },
    "meta": {
      "type": "object",
      "additionalProperties": false,
      "required": ["created_at", "updated_at"],
      "properties": {
        "created_at": { "type": "string", "format": "date-time" },
        "updated_at": { "type": "string", "format": "date-time" },
        "schema_hash": { "type": "string", "pattern": "^sha256:[A-Fa-f0-9]{64}$" }
      }
    }
  }
}
```

## Runtime Constraints

- `nodes.id` duhet të jenë unike.
- `edges.from` dhe `edges.to` duhet të referojnë node ekzistues.
- Nuk lejohet cikël me `depends_on`.
- `integration` nodes duhet të kalojnë validimet e sigurisë së plugin-it (scheme/host/metadata).
- `owner_id` duhet të vijë nga kontekst i besuar server-side, jo nga input i lirë i UI.

## Backward Compatibility Mapping

Për schema ekzistuese (`widgets`, `actions`, `integrations`):

- `widgets[]` -> `nodes[type=widget]`
- `actions[]` -> `nodes[type=action]`
- `widget.source/action` -> `nodes[type=data_source]` + `edges.feeds|triggers`

## Error Codes

- `UI_GRAPH_SCHEMA_INVALID`
- `UI_GRAPH_DUPLICATE_NODE_ID`
- `UI_GRAPH_EDGE_REF_INVALID`
- `UI_GRAPH_DEPENDS_ON_CYCLE`
- `UI_GRAPH_INTEGRATION_POLICY_BLOCKED`
