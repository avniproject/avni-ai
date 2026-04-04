#!/usr/bin/env bash
#
# dify-manage.sh — Manage Dify workflows from the terminal via Console API
#
# Usage:
#   ./dify-manage.sh login                   # Authenticate and save token
#   ./dify-manage.sh export [app_id]         # Export workflow DSL to YAML
#   ./dify-manage.sh import <file.yml>       # Import DSL as new app
#   ./dify-manage.sh list                    # List all apps
#   ./dify-manage.sh publish [app_id]        # Publish a workflow
#   ./dify-manage.sh diff [app_id]           # Diff remote vs local DSL
#   ./dify-manage.sh pull [app_id]           # Export and overwrite local file
#   ./dify-manage.sh push <file.yml>         # Import DSL and confirm
#
# Config: Set these env vars or use a .env file in the same directory
#   DIFY_HOST       (default: https://cloud.dify.ai)
#   DIFY_EMAIL      (your Dify login email)
#   DIFY_APP_ID     (default app ID for export/publish/diff/pull)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"
TOKEN_FILE="${SCRIPT_DIR}/.dify-token"
COOKIE_FILE="${SCRIPT_DIR}/.dify-cookies"
CSRF_TOKEN_FILE="${SCRIPT_DIR}/.dify-csrf"

# ── Defaults ──────────────────────────────────────────────
DIFY_HOST="${DIFY_HOST:-https://cloud.dify.ai}"
DIFY_APP_ID="${DIFY_APP_ID:-bb911e64-b52e-49d1-9469-47ec04c19531}"
DIFY_APP_NAME="${DIFY_APP_NAME:-App Configurator [Staging] v3}"

# ── Load .env if present ──────────────────────────────────
if [[ -f "$ENV_FILE" ]]; then
    # shellcheck disable=SC1090
    source "$ENV_FILE"
fi

# ── Helpers ───────────────────────────────���───────────────
red()    { printf '\033[0;31m%s\033[0m\n' "$*"; }
green()  { printf '\033[0;32m%s\033[0m\n' "$*"; }
yellow() { printf '\033[0;33m%s\033[0m\n' "$*"; }
bold()   { printf '\033[1m%s\033[0m\n' "$*"; }

check_deps() {
    for cmd in curl jq; do
        if ! command -v "$cmd" &>/dev/null; then
            red "Error: '$cmd' is required but not installed."
            exit 1
        fi
    done
}

check_cookies() {
    if [[ ! -f "$COOKIE_FILE" ]]; then
        red "No cookies found. Run '$0 login' first."
        exit 1
    fi
    # Check if cookies are expired by examining the access token expiry
    local exp
    exp=$(grep "__Host-access_token" "$COOKIE_FILE" 2>/dev/null | awk '{print $5}')
    if [[ -n "$exp" && "$exp" -lt "$(date +%s)" ]]; then
        yellow "Cookies expired. Run '$0 login' to refresh."
        exit 1
    fi
}

get_csrf_token() {
    grep "__Host-csrf_token" "$COOKIE_FILE" 2>/dev/null | awk '{print $NF}'
}

api() {
    local method="$1" path="$2"
    shift 2
    check_cookies
    local csrf
    csrf=$(get_csrf_token)
    curl -s -X "$method" "${DIFY_HOST}/console/api${path}" \
        -b "$COOKIE_FILE" \
        -H "X-Csrf-Token: ${csrf}" \
        -H "Content-Type: application/json" \
        "$@"
}

resolve_app_id() {
    echo "${1:-$DIFY_APP_ID}"
}

local_dsl_path() {
    echo "${SCRIPT_DIR}/${DIFY_APP_NAME}.yml"
}

# ── Commands ──────────────────────────────────────────────

do_login() {
    local source="${DIFY_COOKIES_FILE:-$HOME/Downloads/cookies.txt}"

    bold "Importing Dify cookies..."

    if [[ ! -f "$source" ]]; then
        red "Cookie file not found: ${source}"
        echo ""
        echo "To export cookies from your browser:"
        echo "  1. Install a browser extension like 'Get cookies.txt LOCALLY'"
        echo "  2. Go to https://cloud.dify.ai and log in"
        echo "  3. Export cookies to ~/Downloads/cookies.txt"
        echo ""
        echo "Or set DIFY_COOKIES_FILE to your cookies.txt path."
        exit 1
    fi

    # Extract Dify cookies into our cookie jar
    echo "# Netscape HTTP Cookie File" > "$COOKIE_FILE"
    grep "cloud.dify.ai" "$source" >> "$COOKIE_FILE" 2>/dev/null

    local cookie_count
    cookie_count=$(grep -c "cloud.dify.ai" "$COOKIE_FILE" 2>/dev/null || echo 0)

    if [[ "$cookie_count" -eq 0 ]]; then
        red "No cloud.dify.ai cookies found in ${source}"
        exit 1
    fi

    chmod 600 "$COOKIE_FILE"
    green "Imported ${cookie_count} cookies from ${source}"

    # Verify they work
    bold "Testing connection..."
    local response
    response=$(api GET "/apps?page=1&limit=1")
    local total
    total=$(echo "$response" | jq -r '.total // empty' 2>/dev/null)

    if [[ -n "$total" ]]; then
        green "Authenticated! You have ${total} apps."
    else
        red "Cookies don't seem to work:"
        echo "$response" | jq . 2>/dev/null || echo "$response"
        rm -f "$COOKIE_FILE"
        exit 1
    fi
}

do_list() {
    bold "Listing apps..."
    local page=1
    local has_more=true

    printf "%-40s %-30s %-15s\n" "APP ID" "NAME" "MODE"
    printf "%-40s %-30s %-15s\n" "------" "----" "----"

    while [[ "$has_more" == "true" ]]; do
        local response
        response=$(api GET "/apps?page=${page}&limit=30")

        echo "$response" | jq -r '.data[] | [.id, .name, .mode] | @tsv' | \
            while IFS=$'\t' read -r id name mode; do
                printf "%-40s %-30s %-15s\n" "$id" "$name" "$mode"
            done

        has_more=$(echo "$response" | jq -r '.has_more')
        page=$((page + 1))
    done
}

do_export() {
    local app_id
    app_id=$(resolve_app_id "${1:-}")
    local output="${2:-}"

    bold "Exporting app ${app_id}..."
    local response
    response=$(api GET "/apps/${app_id}/export?include_secret=false")

    local yaml_content
    yaml_content=$(echo "$response" | jq -r '.data // empty')

    if [[ -z "$yaml_content" ]]; then
        red "Export failed:"
        echo "$response" | jq . 2>/dev/null || echo "$response"
        exit 1
    fi

    if [[ -n "$output" ]]; then
        echo "$yaml_content" > "$output"
        green "Exported to ${output}"
    else
        echo "$yaml_content"
    fi
}

do_import() {
    local file="$1"
    local name="${2:-}"

    if [[ ! -f "$file" ]]; then
        red "File not found: $file"
        exit 1
    fi

    bold "Importing ${file}..."

    # Read YAML content and create JSON payload using temp file to avoid arg length limits
    local temp_json
    temp_json=$(mktemp)
    
    jq -n \
        --rawfile yaml "$file" \
        --arg name "$name" \
        '{
            mode: "yaml-content",
            yaml_content: $yaml,
            name: (if $name != "" then $name else null end)
        }' > "$temp_json"
    
    local json_payload
    json_payload=$(cat "$temp_json")
    rm -f "$temp_json"

    check_cookies
    local csrf
    csrf=$(get_csrf_token)

    local response
    response=$(curl -s -X POST "${DIFY_HOST}/console/api/apps/import" \
        -b "$COOKIE_FILE" \
        -H "X-Csrf-Token: ${csrf}" \
        -H "Content-Type: application/json" \
        -d "$json_payload")

    local import_id app_id status
    import_id=$(echo "$response" | jq -r '.id // empty')
    app_id=$(echo "$response" | jq -r '.app_id // empty')
    status=$(echo "$response" | jq -r '.status // empty')

    if [[ -z "$import_id" && -z "$app_id" ]]; then
        red "Import failed:"
        echo "$response" | jq . 2>/dev/null || echo "$response"
        exit 1
    fi

    # If import needs confirmation (dependency check)
    if [[ "$status" == "pending" && -n "$import_id" ]]; then
        yellow "Import pending — checking dependencies..."
        local deps
        deps=$(api POST "/apps/imports/${import_id}/check-dependencies")
        echo "$deps" | jq .

        bold "Confirming import..."
        local confirm
        confirm=$(api POST "/apps/imports/${import_id}/confirm")
        app_id=$(echo "$confirm" | jq -r '.app_id // empty')
    fi

    if [[ -n "$app_id" ]]; then
        green "Imported successfully!"
        echo "  App ID:  ${app_id}"
        echo "  URL:     ${DIFY_HOST}/app/${app_id}/workflow"
    else
        yellow "Import response:"
        echo "$response" | jq .
    fi
}

do_publish() {
    local app_id
    app_id=$(resolve_app_id "${1:-}")

    bold "Publishing workflow for ${app_id}..."
    local response
    response=$(api POST "/apps/${app_id}/workflows/publish")

    local result
    result=$(echo "$response" | jq -r '.result // empty')

    if [[ "$result" == "success" ]]; then
        green "Workflow published successfully!"
    else
        yellow "Publish response:"
        echo "$response" | jq . 2>/dev/null || echo "$response"
    fi
}

do_diff() {
    local app_id
    app_id=$(resolve_app_id "${1:-}")
    local local_file
    local_file=$(local_dsl_path)

    if [[ ! -f "$local_file" ]]; then
        red "Local file not found: ${local_file}"
        exit 1
    fi

    bold "Fetching remote DSL for diff..."
    local tmp_remote
    tmp_remote=$(mktemp /tmp/dify-remote-XXXXXX.yml)
    do_export "$app_id" "$tmp_remote"

    if command -v diff &>/dev/null; then
        echo ""
        bold "Diff: LOCAL (left) vs REMOTE (right)"
        echo "─────────────────────────────────────"
        diff --color=auto -u "$local_file" "$tmp_remote" || true
    fi

    rm -f "$tmp_remote"
}

do_pull() {
    local app_id
    app_id=$(resolve_app_id "${1:-}")
    local local_file
    local_file=$(local_dsl_path)

    do_export "$app_id" "$local_file"
    green "Pulled remote DSL → ${local_file}"
}

do_push() {
    local file="${1:-$(local_dsl_path)}"
    do_import "$file"
}

do_update() {
    local app_id="${1:-}"
    local file="${2:-}"

    if [[ -z "$app_id" ]]; then
        red "Usage: $0 update <app_id> <file.yml>"
        exit 1
    fi

    if [[ -z "$file" || ! -f "$file" ]]; then
        red "File not found: ${file}"
        exit 1
    fi

    bold "Updating workflow for app ${app_id}..."

    # Convert YAML to JSON structure that Dify expects
    local temp_yaml temp_json
    temp_yaml=$(mktemp)
    temp_json=$(mktemp)
    
    # Parse YAML to JSON
    python3 -c "import yaml, json, sys; print(json.dumps(yaml.safe_load(open('$file'))))" > "$temp_yaml" 2>/dev/null || {
        red "Failed to parse YAML. Make sure Python3 with PyYAML is installed."
        rm -f "$temp_yaml" "$temp_json"
        exit 1
    }
    
    # Extract graph and features from parsed YAML
    jq '{
        graph: .workflow.graph,
        features: .workflow.features,
        environment_variables: (.workflow.environment_variables // []),
        conversation_variables: (.workflow.conversation_variables // [])
    }' "$temp_yaml" > "$temp_json"

    check_cookies
    local csrf
    csrf=$(get_csrf_token)

    # Update the workflow DSL
    local response
    response=$(curl -s -X POST "${DIFY_HOST}/console/api/apps/${app_id}/workflows/draft" \
        -b "$COOKIE_FILE" \
        -H "X-Csrf-Token: ${csrf}" \
        -H "Content-Type: application/json" \
        -d @"$temp_json")

    rm -f "$temp_yaml" "$temp_json"

    # Check if update was successful
    if echo "$response" | jq -e '.result == "success"' >/dev/null 2>&1; then
        green "Workflow updated successfully!"
        echo "  App ID:  ${app_id}"
        echo "  URL:     ${DIFY_HOST}/app/${app_id}/workflow"
        echo ""
        yellow "Don't forget to publish the changes!"
    else
        red "Update failed:"
        echo "$response" | jq . 2>/dev/null || echo "$response"
        exit 1
    fi
}

# ── Main ──────────────────────────────────────────────────

check_deps

case "${1:-help}" in
    login)
        do_login
        ;;
    list|ls)
        do_list
        ;;
    export)
        do_export "${2:-}" "${3:-}"
        ;;
    import)
        if [[ -z "${2:-}" ]]; then
            red "Usage: $0 import <file.yml> [name]"
            exit 1
        fi
        do_import "$2" "${3:-}"
        ;;
    publish|pub)
        do_publish "${2:-}"
        ;;
    diff)
        do_diff "${2:-}"
        ;;
    pull)
        do_pull "${2:-}"
        ;;
    push)
        do_push "${2:-}"
        ;;
    update)
        if [[ -z "${2:-}" || -z "${3:-}" ]]; then
            red "Usage: $0 update <app_id> <file.yml>"
            exit 1
        fi
        do_update "$2" "$3"
        ;;
    help|--help|-h)
        bold "dify-manage.sh — Manage Dify workflows from the terminal"
        echo ""
        echo "Commands:"
        echo "  login                    Import cookies from browser export"
        echo "  list, ls                 List all apps"
        echo "  export [app_id] [file]   Export DSL (default: your v3 workflow)"
        echo "  import <file> [name]     Import DSL as new app"
        echo "  publish, pub [app_id]    Publish a workflow"
        echo "  diff [app_id]            Diff remote vs local DSL"
        echo "  update <app_id> <file>   Update existing app's workflow DSL"
        echo "  pull [app_id]            Download remote DSL to local file"
        echo "  push [file]              Upload local DSL to Dify"
        echo ""
        echo "Config (.env or env vars):"
        echo "  DIFY_HOST       Default: https://cloud.dify.ai"
        echo "  DIFY_EMAIL      Your login email"
        echo "  DIFY_PASSWORD   Your login password"
        echo "  DIFY_APP_ID     Default: bb911e64-b52e-49d1-9469-47ec04c19531"
        echo "  DIFY_APP_NAME   Default: App Configurator [Staging] v3"
        echo ""
        echo "Examples:"
        echo "  $0 login"
        echo "  $0 list"
        echo "  $0 pull                          # Download your v3 workflow"
        echo "  $0 diff                          # Compare local vs remote"
        echo "  $0 export abc-123 out.yml        # Export specific app"
        echo "  $0 push                          # Upload local DSL"
        ;;
    *)
        red "Unknown command: $1"
        echo "Run '$0 help' for usage."
        exit 1
        ;;
esac
